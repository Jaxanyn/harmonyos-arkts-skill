import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ark_device.hdc import DeviceError
from ark_device.planning import discover_deveco, prepare


class PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.home, _ = discover_deveco()
        except DeviceError:
            raise unittest.SkipTest('Local DevEco JSON5 parser is unavailable')

    def setUp(self):
        scratch = Path(__file__).resolve().parents[1] / 'build'
        scratch.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = {'app': {'products': [{'name': 'default', 'signingConfig': 'local'}],
                              'buildModeSet': [{'name': 'debug'}],
                              'signingConfigs': [{'name': 'local', 'material': dict.fromkeys(['storePassword'], 'PRIVATE_TEST_VALUE')}]},
                       'modules': [{'name': 'entry', 'srcPath': './entry'}]}
        (self.root / 'entry/src/main').mkdir(parents=True)
        (self.root / 'AppScope').mkdir()
        (self.root / 'AppScope/app.json5').write_text('{app:{bundleName:"com.example.app",},}')
        (self.root / 'entry/src/main/module.json5').write_text('{module:{name:"entry",type:"entry",mainElement:"Start",abilities:[{name:"Start"}]}}')
        (self.root / 'entry/build-profile.json5').write_text('{targets:[{name:"default"}]}')

    def run_prepare(self, **options):
        (self.root / 'build-profile.json5').write_text('// valid JSON5\n' + json.dumps(self.config))
        return prepare(self.root, deveco=str(self.home), **options)

    def test_plan_uses_registered_entry_and_excludes_secrets(self):
        result = self.run_prepare()
        self.assertEqual(result['ability'], 'Start')
        self.assertEqual(result['module'], 'entry')
        self.assertNotIn('PRIVATE_TEST_VALUE', json.dumps(result))
        self.assertNotIn('material', json.dumps(result))
        self.assertEqual(result['build_mode'], 'debug')

    def test_ambiguous_product_requires_selection(self):
        self.config['app']['products'].append({'name': 'other', 'signingConfig': 'local'})
        with self.assertRaises(DeviceError) as caught:
            self.run_prepare()
        self.assertIn('Select product', str(caught.exception))
        self.assertEqual(self.run_prepare(product='other')['product'], 'other')

    def test_multiple_entry_modules_require_selection(self):
        import shutil
        shutil.copytree(self.root / 'entry', self.root / 'demo')
        (self.root / 'demo/src/main/module.json5').write_text('{module:{name:"demo",type:"entry",mainElement:"Start",abilities:[{name:"Start"}]}}')
        self.config['modules'].append({'name': 'demo', 'srcPath': './demo'})
        with self.assertRaisesRegex(DeviceError, 'Select entry module'):
            self.run_prepare()
        self.assertEqual(self.run_prepare(module='demo')['module'], 'demo')

    def test_multiple_targets_require_selection(self):
        (self.root / 'entry/build-profile.json5').write_text('{targets:[{name:"default"},{name:"tablet"}]}')
        with self.assertRaisesRegex(DeviceError, 'Select target'):
            self.run_prepare()
        self.assertEqual(self.run_prepare(target='tablet')['target'], 'tablet')

    def test_custom_hap_path_is_preserved(self):
        self.assertEqual(self.run_prepare(hap='artifacts/custom-signed.hap')['hap'],
                         'artifacts/custom-signed.hap')

    def test_unregistered_example_is_not_selected(self):
        p = self.root / 'example/src/main'
        p.mkdir(parents=True)
        (p / 'module.json5').write_text('{module:{name:"example",type:"entry"}}')
        self.assertEqual(self.run_prepare()['module'], 'entry')

    def test_unsigned_product_is_blocked(self):
        self.config['app']['products'][0].pop('signingConfig')
        with self.assertRaises(DeviceError):
            self.run_prepare()

    def test_target_product_mapping_is_enforced(self):
        self.config['modules'][0]['targets'] = [{'name': 'default', 'applyToProducts': ['other']}]
        with self.assertRaises(DeviceError):
            self.run_prepare()

    def test_escaping_module_is_blocked(self):
        self.config['modules'][0]['srcPath'] = '..'
        with self.assertRaises(DeviceError):
            self.run_prepare()

    def test_parse_error_does_not_echo_signing_content(self):
        (self.root / 'build-profile.json5').write_text('{PRIVATE_TEST_VALUE:')
        with self.assertRaises(DeviceError) as caught:
            prepare(self.root, deveco=str(self.home))
        self.assertNotIn('PRIVATE_TEST_VALUE', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
