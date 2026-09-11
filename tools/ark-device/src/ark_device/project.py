"""Reviewed project build plans composed with the existing device adapter."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

from .cli import bounded_float, byte_limit, log_level, log_regex, log_tags
from .hdc import DeviceError, Hdc, inspect_hap
from .process import CommandCancelled, execute
from .session import capture_session, evaluate_acceptance, save_report


def inspect_project(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir() or not (root / 'build-profile.json5').is_file():
        raise DeviceError('PROJECT_NOT_FOUND', 'Expected a HarmonyOS project with build-profile.json5')
    modules = []
    # Discovery is a candidate list, not a substitute for the active product configuration.
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in ('build', 'oh_modules', 'node_modules')
                   and not d.startswith('.') and not (Path(current) / d).is_symlink()]
        if 'module.json5' in files:
            modules.append(str((Path(current) / 'module.json5').relative_to(root)))
    return {'project': str(root), 'module_candidates': sorted(modules),
            'selection': 'Read active product/target and module metadata before creating a plan'}


def default_evidence_directory(root):
    """Keep large HAP evidence off a potentially full system temporary drive."""
    try:
        base = root.parent / '.ark-evidence'
        base.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix='ark-project-', dir=base))
    except OSError:
        return Path(tempfile.mkdtemp(prefix='ark-project-'))


def load_plan(path):
    plan = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(plan, dict):
        raise ValueError('Build plan must be an object')
    required = ('project', 'argv', 'hap', 'bundle', 'module', 'ability', 'product', 'target', 'build_mode')
    if any(k not in plan for k in required):
        raise ValueError('Build plan requires ' + ', '.join(required))
    if any(not isinstance(plan[k], str) or not plan[k].strip() for k in required if k != 'argv'):
        raise ValueError('Plan identifiers and paths must be nonempty strings')
    root = Path(plan['project'])
    if not root.is_absolute():
        raise ValueError('Project path must be absolute')
    root = root.resolve(strict=True)
    inspect_project(root)
    argv = plan['argv']
    if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
        raise ValueError('argv must be a nonempty string array')
    executable = Path(argv[0])
    if not executable.is_absolute() or not executable.is_file() or executable.suffix.lower() in ('.bat', '.cmd'):
        raise ValueError('Use an absolute executable path, not a shell script wrapper')
    hap = Path(plan['hap'])
    if hap.is_absolute():
        raise ValueError('hap must be relative to the project')
    hap = (root / hap).resolve()
    if not hap.is_relative_to(root) or hap.suffix.lower() != '.hap':
        raise ValueError('HAP must remain inside the project')
    env = plan.get('env', {})
    if not isinstance(env, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in env.items()):
        raise ValueError('env must contain string values')
    if any(k.upper() not in ('JAVA_HOME', 'DEVECO_SDK_HOME', 'PATH') for k in env):
        raise ValueError('Only JAVA_HOME, DEVECO_SDK_HOME and PATH overrides are supported; no signing secrets')
    from .hdc import identifier
    for field in ('bundle', 'module', 'ability', 'product', 'target'):
        identifier(plan[field], field)
    return plan, root, hap


def build(plan, root, hap, directory, timeout, result):
    before = inspect_hap(hap)['sha256'] if hap.exists() else None
    env = os.environ.copy()
    env.update(plan.get('env', {}))
    if env.get('JAVA_HOME'):
        env['PATH'] = str(Path(env['JAVA_HOME']) / 'bin') + os.pathsep + env.get('PATH', '')
    result['build'] = {'status': 'running', 'project': str(root),
                       'target': {k: plan[k] for k in ('product', 'target', 'module', 'build_mode')},
                       'previous_hap_sha256': before,
                       'java': shutil.which('java', path=env.get('PATH', '')),
                       'executable': plan['argv'][0]}
    cancelled = None
    try:
        evidence = execute(plan['argv'], timeout=timeout, limit=10 * 1024 * 1024, cwd=str(root), env=env)
    except CommandCancelled as error:
        evidence = error.evidence
        cancelled = error
    (directory / 'build.log').write_text(evidence['output'], encoding='utf-8')
    result['build'].update({k: v for k, v in evidence.items() if k != 'output'})
    result['build']['log'] = str(directory / 'build.log')
    result['build']['status'] = 'cancelled' if cancelled else 'failed'
    if cancelled:
        raise cancelled
    if evidence['timed_out'] or evidence['truncated'] or evidence['exit_code'] != 0:
        raise DeviceError('BUILD_FAILED', 'Build failed, timed out or exceeded output limit; no HAP was installed')
    info = inspect_hap(hap)
    if (info['bundle'] != plan['bundle'] or info['module'] != plan['module'] or
            plan['ability'] not in info['abilities']):
        raise DeviceError('TARGET_MISMATCH', 'Built HAP does not match the reviewed launch target')
    result['build'].update(status='passed', artifact_changed=before != info['sha256'])
    result['hap'] = info
    # Freeze the verified bytes for installation; incremental successful builds may reuse output.
    frozen = directory / 'application.hap'
    shutil.copyfile(hap, frozen)
    if inspect_hap(frozen)['sha256'] != info['sha256']:
        raise DeviceError('ARTIFACT_CHANGED', 'HAP changed while copying; no installation attempted')
    return {**info, 'path': str(frozen)}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Inspect projects or execute an explicitly reviewed build-and-run plan')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('inspect').add_argument('--project', required=True)
    run = commands.add_parser('run')
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument('--plan', help='reviewed JSON build plan; executes project code')
    source.add_argument('--project', help='prepare a standard debug build from project configuration')
    prepare_cmd = commands.add_parser('prepare')
    prepare_cmd.add_argument('--project', required=True)
    prepare_cmd.add_argument('--output', type=Path, help='new plan file; default is a temporary file')
    for command in (run, prepare_cmd):
        for name in ('deveco', 'product', 'module', 'target', 'ability', 'hap'):
            command.add_argument('--' + name)
    run.add_argument('--hdc')
    run.add_argument('--device')
    run.add_argument('--output', type=Path)
    run.add_argument('--build-timeout', type=bounded_float, default=600)
    run.add_argument('--install-timeout', type=bounded_float, default=180)
    run.add_argument('--seconds', type=bounded_float, default=30)
    run.add_argument('--max-bytes', type=byte_limit, default=10 * 1024 * 1024)
    run.add_argument('--level', type=log_level, help='comma-separated HiLog levels, for example E,W')
    run.add_argument('--tag', type=log_tags, help='comma-separated HiLog tags, up to 10')
    run.add_argument('--regex', type=log_regex, help='HiLog regular expression, up to 256 characters')
    run.add_argument('--acceptance', type=Path, help='JSON no-UI assertions for logs and stable process')
    args = parser.parse_args(argv)
    if args.command == 'run' and args.plan and any(getattr(args, k) for k in ('deveco', 'product', 'module', 'target', 'ability', 'hap')):
        parser.error('Selection overrides apply only to --project; edit and review the explicit plan instead')
    result = {'schema_version': 1, 'started_at': datetime.now(timezone.utc).isoformat(), 'operation': 'project-' + args.command, 'status': 'failed', 'business_acceptance': 'not-run',
              'limitations': ['Build plans execute project code and must be reviewed before use',
                              'No uninstall, signing replacement, dependency installation or automatic source repair',
                              'Successful build task is trusted; source-to-binary reproducibility is not proven',
                              'Build timeout stops its client; descendants may remain, inspect before retry']}
    directory = None
    hdc = None
    code = 1
    try:
        if args.command == 'inspect':
            result.update(inspect_project(args.project), status='passed')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == 'prepare' or args.project:
            from .planning import prepare
            plan = prepare(args.project, **{k: getattr(args, k) for k in ('deveco', 'product', 'module', 'target', 'ability', 'hap')})
            if args.command == 'prepare':
                if args.output:
                    file = args.output.resolve()
                    with file.open('x', encoding='utf-8') as stream:
                        json.dump(plan, stream, ensure_ascii=False, indent=2)
                else:
                    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json', prefix='ark-plan-', delete=False) as stream:
                        json.dump(plan, stream, ensure_ascii=False, indent=2)
                        file = Path(stream.name)
                load_plan(file)
                print(json.dumps({'status': 'prepared', 'plan_path': str(file), 'target': {k: plan[k] for k in ('bundle', 'module', 'ability', 'product', 'target')}}, ensure_ascii=False, indent=2))
                return 0
        if args.output:
            args.output.mkdir(parents=True, exist_ok=False)
            directory = args.output.resolve()
        else:
            evidence_root = Path(plan['project']).resolve(strict=True) if args.project else load_plan(args.plan)[1]
            directory = default_evidence_directory(evidence_root)
        plan_path = args.plan
        if args.project:
            plan_path = directory / 'plan.json'
            plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
        plan, root, hap = load_plan(plan_path)
        result['bundle'] = plan['bundle']
        hdc = Hdc(args.hdc)
        hdc.select(args.device)
        hdc.check_capabilities()
        package = build(plan, root, hap, directory, args.build_timeout, result)
        result['install'] = {'status': 'running'}
        result['install'] = hdc.install(package, args.install_timeout)
        capture_session(hdc, plan['bundle'], args.seconds, args.max_bytes, directory, result,
                        lambda: hdc.launch(plan['bundle'], plan['ability'], plan['module']),
                        levels=args.level, tags=args.tag, regex=args.regex)
        evaluate_acceptance(args.acceptance, result)
        result['status'] = 'passed'
        code = 0
    except KeyboardInterrupt:
        result['status'] = 'cancelled'
        result['error'] = {'code': 'CANCELLED', 'message': 'Cancelled; inspect build/device state before retry'}
        code = 130
    except (OSError, ValueError, RuntimeError, DeviceError) as error:
        result['error'] = {'code': getattr(error, 'code', 'LOCAL_ERROR'), 'message': str(error)}
    for stage in ('build', 'install'):
        if result.get(stage, {}).get('status') == 'running':
            result[stage]['status'] = 'cancelled' if code == 130 else 'failed'
    if directory:
        print(save_report(directory, result, hdc.evidence if hdc else [], hdc.device if hdc else None))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
