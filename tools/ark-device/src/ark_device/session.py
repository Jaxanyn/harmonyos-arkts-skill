"""One bounded log session; never persist the unfiltered app stream."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time

from .hdc import DeviceError
from .process import Capture


def redact(text, device=None):
    if device:
        text = text.replace(device, "<device>")
    return re.sub(r"(?i)(token|password|secret|authorization|api[_-]?key)([\s\"':=]+)[^\s,}]+",
                  r"\1\2<redacted>", text)


def select_logs(text, pids, cutoff):
    selected = []
    for line in text.splitlines():
        fields = line.split(maxsplit=4)
        if len(fields) < 5 or fields[1] not in pids:
            continue
        try:
            timestamp = float(fields[0])
        except ValueError:
            continue
        if timestamp >= cutoff:
            selected.append(line)
    return selected


def map_authorization(lines):
    """Observed Map Kit messages only; internal reply codes are not auth verdicts."""
    passed = failed = 0
    for line in lines:
        if not re.search(r"/OHMapSDK_(?:MapComponent|Mapview):", line):
            continue
        passed += bool(re.search(r"\bcheckMapPermission:\s*true\b", line))
        failed += bool(re.search(r"\bcheckMapPermission:\s*false\b", line) or
                       "The app does not have map permission" in line)
    status = "mixed" if passed and failed else "passed" if passed else "failed" if failed else "not-observed"
    return {"status": status, "positive_lines": passed, "negative_lines": failed,
            "scope": "observed SDK log messages only; not business acceptance or a root-cause diagnosis"}


def classify_errors(lines):
    patterns = (
        ('permission', r'permission denied|does not have map permission|\bcode[=: ]*201\b'),
        ('native', r'\bnapi\b|\bnative\b|\bdlopen\b|\.so\b'),
        ('storage', r'\bsqlite\b|\bdatabase\b|\bstorage\b|\bfile\b|path not exist'),
        ('network', r'\bnetwork\b|\bnet(?:work)?(?:connection|quality)?\b'),
        ('map', r'\bmap(?:render|view|kit)?\b'),
    )
    groups = {}
    for line in lines:
        name = next((label for label, pattern in patterns if re.search(pattern, line, re.I)), 'unknown')
        item = groups.setdefault(name, {'count': 0, 'example': line})
        item['count'] += 1
    return groups


def capture_session(hdc, bundle, seconds, limit, directory, result, launch=None, *, levels=None, tags=None, regex=None):
    clock = hdc.call(["shell", "date", "+%s"]).strip()
    if not re.fullmatch(r"\d{10,}", clock):
        raise DeviceError("DEVICE_CLOCK_UNKNOWN", "Cannot exclude buffered logs without device epoch time")
    cutoff = int(clock)
    before = hdc.pids(bundle)
    if launch is None and not before:
        raise DeviceError("APP_NOT_RUNNING", "Start the application before capturing its logs")
    args = ["shell", "hilog", "-t", "app", "-v", "epoch"]
    if levels:
        args += ['-L', levels]
    if tags:
        args += ['-T', tags]
    if regex:
        args += ['-e', regex]
    if launch is None:
        args += ["-P", ",".join(before)]
    argv = hdc.argv(args)
    capture = Capture(argv, limit)
    pids = set(before)
    logs = {"status": "not-run", "requested_seconds": seconds, "argv": argv,
            "device_epoch_cutoff": cutoff, "time_precision": "one second",
            "scope": "observed main process IDs; child processes not covered",
            "filter": {'levels': levels, 'tags': tags, 'regex': regex},
            "raw_stream_persisted": False}
    result["logs"] = logs
    failure = None
    final = []
    started = time.monotonic()
    try:
        # Ensure the collector did not immediately fail; no log-clearing side effect.
        time.sleep(0.2)
        if capture.truncated:
            raise DeviceError("LOG_LIMIT", "Log capture reached its byte limit")
        if capture.process.poll() is not None:
            raise DeviceError("LOG_STREAM_ENDED", "HiLog exited before observation")
        if launch:
            result["launch"] = launch()
        initial = hdc.pids(bundle)
        pids.update(initial)
        result["process_initial"] = initial
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if capture.truncated:
                raise DeviceError("LOG_LIMIT", "Log capture reached its byte limit")
            if capture.process.poll() is not None:
                raise DeviceError("LOG_STREAM_ENDED", "HiLog ended before the requested duration")
            time.sleep(min(0.1, max(0, deadline - time.monotonic())))
        final = hdc.pids(bundle)
        pids.update(final)
        result["process_final"] = final
        result["process_observation"] = {
            "status": "passed" if initial and final and initial == final else "failed",
            "criterion": "main process observed after launch and at the end; not continuous liveness",
            "pid_changed": initial != final,
        }
        if not initial or not final:
            raise DeviceError("APP_NOT_RUNNING", "Target process missing at an observation point")
        if initial != final:
            raise DeviceError("PROCESS_CHANGED", "Target process IDs changed during observation")
    except BaseException as error:
        failure = error
    finally:
        logs["collector_exit_before_stop"] = capture.process.poll()
        text = capture.finish()
        if failure is None and capture.truncated:
            failure = DeviceError("LOG_LIMIT", "Log capture reached its byte limit")
        if failure is None and logs["collector_exit_before_stop"] is not None:
            failure = DeviceError("LOG_STREAM_ENDED", "HiLog ended before the collector was stopped")
        selected = select_logs(text, pids, cutoff)
        (directory / "target.log").write_text("\n".join(selected), encoding="utf-8")
        filtered = bool(levels or tags or regex)
        logs.update({"elapsed_seconds": round(time.monotonic() - started, 3),
                     "status": "cancelled" if isinstance(failure, KeyboardInterrupt) else "passed" if (selected or filtered) and failure is None else "failed",
                     "lines": len(selected), "truncated": capture.truncated,
                     "path": str(directory / "target.log"), "collector_stopped": True})
        logs["device_dropped_lines_observed"] = sum(
            int(match.group(1)) for line in selected
            if (match := re.search(r"/HiLog:.*?\b(\d+) line\(s\) dropped!", line)))
        error_lines = [line for line in selected if re.search(r"\s[EF]\s", line)]
        result["diagnostics"] = {
            "error_level_lines": len(error_lines),
            "categories": classify_errors(error_lines),
            "map_authorization": map_authorization(selected),
            "interpretation": "log severity only, not confirmed bugs or acceptance results",
            "excerpt": redact("\n".join(error_lines[-10:])[-4000:], hdc.device),
        }
        if not selected and failure is None and not filtered:
            failure = DeviceError("NO_TARGET_LOGS", "No target logs observed; capture is not verified")
    if failure:
        raise failure


def capture_coverage(logs):
    """Coverage of the observed stream, never a guarantee that every event was logged."""
    if not logs or logs.get('status') == 'not-run':
        return 'not-run'
    if (logs.get('status') != 'passed' or logs.get('truncated') is True or
            logs.get('device_dropped_lines_observed', 0) > 0):
        return 'partial'
    if (logs.get('truncated') is not False or not logs.get('lines') or
            'device_dropped_lines_observed' not in logs):
        return 'unknown'
    return 'bounded-window'


def evaluate_acceptance(path, result):
    if not path:
        return
    try:
        config = json.loads(Path(path).read_text(encoding='utf-8'))
        required = config.get('required_log_patterns', [])
        forbidden = config.get('forbidden_log_patterns', [])
        stable = config.get('require_stable_process', False)
        if (not isinstance(config, dict) or not isinstance(required, list) or not isinstance(forbidden, list) or
                not isinstance(stable, bool) or len(required) > 10 or len(forbidden) > 10 or
                any(not isinstance(item, str) or not 1 <= len(item) <= 256 for item in required + forbidden)):
            raise ValueError
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise DeviceError('INVALID_ACCEPTANCE_CONFIG', 'Acceptance config must use bounded JSON string pattern lists') from error
    logs = result.get('logs', {})
    coverage = capture_coverage(logs)
    text = Path(logs['path']).read_text(encoding='utf-8')
    missing = [item for item in required if not re.search(item, text)]
    present = [item for item in forbidden if re.search(item, text)]
    process_ok = not stable or result.get('process_observation', {}).get('status') == 'passed'
    result['business_acceptance'] = ('blocked' if coverage != 'bounded-window' else
                                     'failed' if missing or present or not process_ok else 'passed')
    result['acceptance'] = {'coverage': coverage, 'missing_required': missing, 'present_forbidden': present,
                            'stable_process': process_ok, 'scope': 'declared no-UI log and process assertions only'}


def save_report(directory, result, evidence, device):
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    result["commands"] = evidence
    result["report_path"] = str(directory / "report.json")
    stages = ('build', 'install', 'launch', 'process_observation')
    logs = result.get('logs', {})
    coverage = capture_coverage(logs)
    if logs:
        logs['coverage'] = coverage
    rows = ['# Run report', '',
            f"Tool operation: {result.get('status', 'unknown')}. This is not a business verdict.",
            '', '## Execution', '', '| Stage | Result |', '| --- | --- |']
    rows += [f"| {stage} | {result.get(stage, {}).get('status', 'not-run')} |" for stage in stages]
    rows += ['', '## Log capture', '', '| Evidence | Result |', '| --- | --- |',
             f"| Collector | {logs.get('status', 'not-run')} |",
             f"| Coverage | {coverage} |",
             f"| Target lines | {logs.get('lines', 'unknown')} |",
             f"| Byte limit truncation | {logs.get('truncated', 'unknown')} |",
             f"| Device dropped lines observed | {logs.get('device_dropped_lines_observed', 'unknown')} |",
             '', 'bounded-window means the requested observation completed without detected loss; it does not prove every event was logged.',
             'partial or unknown coverage cannot support a no-error conclusion. Drop counts include only recognized warnings in selected target logs.']
    diagnostics = result.get('diagnostics', {})
    auth = diagnostics.get('map_authorization', {}).get('status', 'not-observed')
    rows += ['', '## SDK and log signals', '',
             f"Map authorization: {auth}.",
             f"Error-level lines: {diagnostics.get('error_level_lines', 'unknown')}.",
             'These are observed signals, not confirmed root causes or a business verdict.',
             '', '## Business acceptance', '',
             f"Status: {result.get('business_acceptance', 'not-run')}.",
             'This CLI does not run business assertions. Record each scenario, expected/actual result, evidence and cleanup in a companion acceptance report; preserve this raw report.']
    categories = diagnostics.get('categories', {})
    if categories:
        rows += ['', '## Diagnostic candidates', '']
        rows += [f"- {name}: {item['count']} line(s)." for name, item in sorted(categories.items())]
        rows += ['Categories route the next check; they do not establish a root cause.']
    if result.get('error'):
        rows += ['', 'Error: ' + result['error']['code'], '', redact(result['error']['message'], device)]
    rows += ['', 'Evidence: report.json; build.log and target.log when generated.',
             'Process observations are snapshots. Log signals do not prove business correctness.',
             'Map authorization is SDK log evidence, not an offline-map business verdict. Validate the project data source and tested features separately.']
    (directory / 'report.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    # Reports are local evidence. CLI summaries redact identifiers and omit raw command output.
    (directory / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {k: v for k, v in result.items() if k not in ("commands", "device", "hap")}
    if "logs" in summary:
        summary["logs"] = {k: v for k, v in summary["logs"].items() if k != "argv"}
    def clean(value):
        if isinstance(value, str):
            return redact(value, device)
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()}
        return value
    return json.dumps(clean(summary), ensure_ascii=False, indent=2)
