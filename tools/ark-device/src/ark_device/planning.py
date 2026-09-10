"""Prepare the supported local Hvigor layout; ambiguity fails closed."""
import json
from pathlib import Path
import shutil

from .hdc import DeviceError, identifier
from .process import execute


def discover_deveco(explicit=None):
    if explicit:
        candidates = [Path(explicit)]
    else:
        hdc = shutil.which('hdc')
        candidates = list(Path(hdc).resolve().parents) if hdc else []
    for root in candidates:
        files = {'node': root / 'tools/node/node.exe',
                 'hvigor': root / 'tools/hvigor/bin/hvigorw.js',
                 'json5': root / 'tools/hvigor/hvigor-ohos-plugin/node_modules/json5',
                 'java': root / 'jbr/bin/java.exe'}
        if all(p.exists() for p in files.values()) and (root / 'sdk').is_dir():
            return root.resolve(), files
    raise DeviceError('TOOLCHAIN_REQUIRED', 'Supported Windows DevEco layout not found; supply --deveco or use a reviewed --plan')


def prepare(project, *, deveco=None, product=None, module=None, target=None, ability=None, hap=None):
    root = Path(project).resolve(strict=True)
    home, tools = discover_deveco(deveco)
    options = {k: v for k, v in {'product': product, 'module': module, 'target': target, 'ability': ability}.items() if v}
    for k, v in options.items():
        identifier(v, k)
    result = execute([str(tools['node']), str(Path(__file__).with_name('prepare.cjs')),
                      str(tools['json5']), str(root), json.dumps(options)], timeout=20, limit=65536)
    if result['exit_code'] or result['timed_out'] or result['truncated']:
        raise DeviceError('PLAN_SELECTION_REQUIRED', result['output'].strip() or 'Configuration discovery failed')
    data = json.loads(result['output'])
    for k in ('product', 'module', 'target', 'ability', 'bundle'):
        identifier(data[k], k)
    # Standard Hvigor output convention. Custom layouts must supply --hap or an explicit plan.
    output = hap or str(Path(data.pop('module_path')) / 'build' / data['product'] / 'outputs' /
                        data['target'] / f"{data['module']}-{data['target']}-signed.hap")
    data.pop('module_path', None)
    return {'project': str(root), 'argv': [str(tools['node']), str(tools['hvigor']), '--mode', 'module',
            '-p', f"product={data['product']}", '-p', f"module={data['module']}@{data['target']}",
            '-p', 'buildMode=debug', 'assembleHap', '--no-daemon'],
            'hap': output, **data, 'build_mode': 'debug',
            'env': {'JAVA_HOME': str(home / 'jbr'), 'DEVECO_SDK_HOME': str(home / 'sdk')}}
