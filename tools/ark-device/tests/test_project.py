import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ark_device.project import main, load_plan, build, inspect_project
from ark_device.hdc import DeviceError
from ark_device.process import CommandCancelled


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'build-profile.json5').write_text('{}')
        self.hap = self.root / 'app.hap'
        with zipfile.ZipFile(self.hap, 'w') as z:
            z.writestr('module.json', json.dumps({'app': {'bundleName': 'com.example.app'},
                        'module': {'name': 'entry', 'abilities': [{'name': 'EntryAbility'}]}}))
        self.plan = {'project': str(self.root), 'argv': [sys.executable, '-c', "print('build succeeded')"],
                     'hap': 'app.hap', 'bundle': 'com.example.app', 'module': 'entry',
                     'ability': 'EntryAbility', 'product': 'default', 'target': 'default', 'build_mode': 'debug'}
        self.file = self.root / 'plan.json'
        self.out = self.root / 'output'

    def write(self):
        self.file.write_text(json.dumps(self.plan))

    def test_failed_build_does_not_install_existing_hap(self):
        self.plan['argv'] = [sys.executable, '-c', "print('compiler error');raise SystemExit(1)"]
        self.write()
        with patch('ark_device.project.Hdc') as adapter, patch('ark_device.project.save_report', return_value='{}'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['run', '--plan', str(self.file), '--output', str(self.out)]), 1)
            adapter.return_value.install.assert_not_called()
            adapter.return_value.launch.assert_not_called()
        self.assertIn('compiler error', (self.out / 'build.log').read_text())

    def test_cancelled_build_retains_output_and_never_installs(self):
        self.write()
        evidence = {'argv': self.plan['argv'], 'output': 'compile started', 'exit_code': -1,
                    'timed_out': False, 'truncated': False, 'duration_seconds': .1}
        with patch('ark_device.project.Hdc') as adapter, \
                patch('ark_device.project.execute', side_effect=CommandCancelled(evidence)), \
                patch('ark_device.project.save_report', return_value='{}') as save, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['run', '--plan', str(self.file), '--output', str(self.out)]), 130)
            adapter.return_value.install.assert_not_called()
            self.assertEqual(save.call_args.args[1]['build']['status'], 'cancelled')
        self.assertEqual((self.out / 'build.log').read_text(), 'compile started')

    def test_hap_must_stay_in_project(self):
        self.plan['hap'] = '../other.hap'
        self.write()
        with self.assertRaises(ValueError):
            load_plan(self.file)

    def test_success_records_reused_artifact_and_freezes_copy(self):
        self.out.mkdir()
        result = {}
        package = build(self.plan, self.root, self.hap, self.out, 5, result)
        self.assertFalse(result['build']['artifact_changed'])
        self.hap.write_bytes(b'changed after build')
        self.assertTrue(zipfile.is_zipfile(package['path']))

    def test_build_runs_in_project_with_process_scoped_java(self):
        self.out.mkdir()
        self.plan['env'] = {'JAVA_HOME': str(self.root / 'java')}
        self.plan['argv'] = [sys.executable, '-c', 'import os; print(os.getcwd()); print(os.environ["PATH"].split(os.pathsep)[0])']
        build(self.plan, self.root, self.hap, self.out, 5, {})
        output = (self.out / 'build.log').read_text()
        self.assertIn(str(self.root), output)
        self.assertIn(str(self.root / 'java' / 'bin'), output)

    def test_wrong_target_blocks_before_install(self):
        self.out.mkdir()
        self.plan['bundle'] = 'com.other.app'
        with self.assertRaises(DeviceError) as caught:
            build(self.plan, self.root, self.hap, self.out, 5, {})
        self.assertEqual(caught.exception.code, 'TARGET_MISMATCH')

    def test_timeout_cannot_accept_old_hap(self):
        self.out.mkdir()
        self.plan['argv'] = [sys.executable, '-c', 'import time; time.sleep(10)']
        with self.assertRaises(DeviceError) as caught:
            build(self.plan, self.root, self.hap, self.out, .1, {})
        self.assertEqual(caught.exception.code, 'BUILD_FAILED')

    def test_inspect_ignores_dependencies_and_outputs(self):
        for folder in ('entry/src/main', 'oh_modules/example', 'entry/build/tmp'):
            p = self.root / folder
            p.mkdir(parents=True)
            (p / 'module.json5').write_text('{}')
        self.assertEqual(len(inspect_project(self.root)['module_candidates']), 1)

    def test_no_device_prevents_build(self):
        self.write()
        with patch('ark_device.project.Hdc') as adapter, patch('ark_device.project.build') as builder, patch('ark_device.project.save_report', return_value='{}'), contextlib.redirect_stdout(io.StringIO()):
            adapter.return_value.select.side_effect = DeviceError('NO_DEVICE', 'not connected')
            self.assertEqual(main(['run', '--plan', str(self.file), '--output', str(self.out)]), 1)
            builder.assert_not_called()


if __name__ == '__main__':
    unittest.main()
