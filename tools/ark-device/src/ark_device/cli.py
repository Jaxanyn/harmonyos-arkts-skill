"""CLI entrypoints: installing/running is explicit, never a discovery side effect."""
import argparse
from datetime import datetime, timezone
import math
from pathlib import Path
import tempfile

from .hdc import DeviceError, Hdc, identifier, inspect_hap
from .session import capture_session, evaluate_acceptance, save_report


def bounded_float(value):
    number = float(value)
    if not math.isfinite(number) or not 0 < number <= 600:
        raise argparse.ArgumentTypeError("expected a duration in (0, 600] seconds")
    return number


def byte_limit(value):
    number = int(value)
    if not 1024 <= number <= 50 * 1024 * 1024:
        raise argparse.ArgumentTypeError("expected 1024 to 52428800 bytes")
    return number


def log_level(value):
    values = [item.strip().upper() for item in value.split(',') if item.strip()]
    aliases = {'DEBUG': 'D', 'INFO': 'I', 'WARN': 'W', 'WARNING': 'W', 'ERROR': 'E', 'FATAL': 'F'}
    values = [aliases.get(item, item) for item in values]
    if not values or any(item not in ('D', 'I', 'W', 'E', 'F') for item in values):
        raise argparse.ArgumentTypeError('expected comma-separated D/I/W/E/F levels')
    return ','.join(dict.fromkeys(values))


def log_tags(value):
    values = [item.strip() for item in value.split(',') if item.strip()]
    if not values or len(values) > 10 or any(not __import__('re').fullmatch(r'[A-Za-z0-9_.-]{1,64}', item) for item in values):
        raise argparse.ArgumentTypeError('expected up to 10 comma-separated log tags')
    return ','.join(dict.fromkeys(values))


def log_regex(value):
    if not 1 <= len(value) <= 256:
        raise argparse.ArgumentTypeError('expected a log expression up to 256 characters')
    return value


def parser():
    root = argparse.ArgumentParser(description="Bounded HarmonyOS device operations. No builds, signing or uninstall.")
    root.add_argument("--version", action="version", version="ark-device 0.1.2")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("doctor", "devices", "install", "launch", "run", "logs"):
        command = commands.add_parser(name)
        if name == "logs":
            command = command.add_subparsers(dest="log_action", required=True).add_parser("capture")
        command.add_argument("--hdc", help="HDC executable; otherwise discovered on PATH")
        command.add_argument("--device", help="explicit connection key; one connected device may be auto-selected")
        command.add_argument("--output", type=Path, help="new evidence directory; must not already exist")
        if name in ("install", "run"):
            command.add_argument("--hap", required=True, type=Path)
            command.add_argument("--install-timeout", type=bounded_float, default=180)
        if name in ("launch", "run", "logs"):
            command.add_argument("--bundle", required=True)
        if name in ("launch", "run"):
            command.add_argument("--ability", required=True)
            command.add_argument("--module", required=True)
        if name == "launch":
            command.add_argument("--capture", action="store_true", help="capture logs around launch without installing")
        if name in ("run", "logs", "launch"):
            command.add_argument("--seconds", type=bounded_float, default=30)
            command.add_argument("--max-bytes", type=byte_limit, default=10 * 1024 * 1024)
            command.add_argument("--level", type=log_level, help="comma-separated HiLog levels, for example E,W")
            command.add_argument("--tag", type=log_tags, help="comma-separated HiLog tags, up to 10")
            command.add_argument("--regex", type=log_regex, help="HiLog regular expression, up to 256 characters")
            command.add_argument('--acceptance', type=Path, help='JSON no-UI assertions for logs and stable process')
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    result = {"schema_version": 1, "operation": args.command,
              "started_at": datetime.now(timezone.utc).isoformat(), "status": "failed",
              "business_acceptance": "not-run", "limitations": [
                  "No UI, map, offline or business assertions performed",
                  "No IDE process inspection; this invocation uses command-line tools only",
                  "No uninstall, data reset or automatic rollback; launched apps are left running",
                  "A timed-out or cancelled install may still finish on device; inspect before retry",
              ]}
    hdc = None
    directory = None
    owns_directory = False
    code = 1
    try:
        if args.output:
            directory = args.output.resolve()
            directory.mkdir(parents=True, exist_ok=False)
        else:
            directory = Path(tempfile.mkdtemp(prefix="ark-device-"))
        owns_directory = True
        if hasattr(args, "bundle"):
            identifier(args.bundle, "bundle")
            result["bundle"] = args.bundle
        if hasattr(args, "ability"):
            identifier(args.ability, "ability")
            identifier(args.module, "module")
        if hasattr(args, "hap"):
            result["hap"] = inspect_hap(args.hap)
            if args.command == "run":
                hap = result["hap"]
                if (args.bundle != hap["bundle"] or args.module != hap["module"]
                        or args.ability not in hap["abilities"]):
                    raise DeviceError("TARGET_MISMATCH", "HAP metadata differs from the requested launch target")
        hdc = Hdc(args.hdc)
        result["hdc_version"] = hdc.call(["-v"]).strip()
        if args.command == "devices":
            result["devices"] = hdc.devices()
        elif args.command == "doctor":
            result["devices"] = hdc.devices()
            result["tool_path"] = hdc.executable
            if result["devices"]:
                result["device"] = hdc.select(args.device)
                hdc.check_capabilities()
                result["device_capabilities"] = "required aa/HiLog switches present"
            else:
                result["device_capabilities"] = "not-run: no device"
        else:
            result["device"] = hdc.select(args.device)
            if args.command in ("run", "launch", "logs"):
                hdc.check_capabilities()
            if args.command in ("install", "run"):
                result["install"] = {"status": "running"}
                result["install"] = hdc.install(result["hap"], args.install_timeout)
            if args.command == "launch" and not args.capture:
                result["launch"] = hdc.launch(args.bundle, args.ability, args.module)
                result["observed_pids"] = hdc.pids(args.bundle)
                if not result["observed_pids"]:
                    raise DeviceError("APP_NOT_RUNNING", "Launch accepted, but no target process observed")
            if args.command in ("run", "logs") or (args.command == "launch" and args.capture):
                launch = (lambda: hdc.launch(args.bundle, args.ability, args.module)) if args.command != "logs" else None
                capture_session(hdc, args.bundle, args.seconds, args.max_bytes, directory, result, launch,
                                levels=args.level, tags=args.tag, regex=args.regex)
                evaluate_acceptance(args.acceptance, result)
        result["status"] = "passed"
        code = 0
    except KeyboardInterrupt:
        result["status"] = "cancelled"
        result["error"] = {"code": "CANCELLED", "message": "Cancelled; only this invocation's collector was stopped"}
        code = 130
    except (DeviceError, OSError, ValueError, RuntimeError) as error:
        result["error"] = {"code": getattr(error, "code", "LOCAL_ERROR"), "message": str(error)}
    if result.get("install", {}).get("status") == "running":
        result["install"]["status"] = "cancelled" if code == 130 else "failed"
    if owns_directory:
        try:
            print(save_report(directory, result, hdc.evidence if hdc else [], hdc.device if hdc else None))
        except OSError as error:
            result["status"] = "failed"
            result["error"] = {"code": "REPORT_WRITE_FAILED", "message": str(error)}
            code = 1
        else:
            return code
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code
