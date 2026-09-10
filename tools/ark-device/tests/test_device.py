"""Synthetic commands only: this suite never invokes HDC or a device."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch, Mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ark_device.cli import main
from ark_device.hdc import DeviceError, Hdc, inspect_hap
from ark_device.process import Capture, CommandCancelled, execute
from ark_device.session import capture_session, redact, select_logs, save_report, map_authorization, capture_coverage


def response(output, exit_code=0):
    return {"output": output, "exit_code": exit_code, "timed_out": False,
            "truncated": False, "argv": [], "duration_seconds": 0}


class AdapterTests(unittest.TestCase):
    def adapter(self, output):
        return Hdc(sys.executable, runner=lambda *a, **k: response(output))

    def test_no_device_and_ambiguous_device_are_blocked(self):
        for output, code in [("[Empty]", "NO_DEVICE"), ("one\ntwo", "DEVICE_REQUIRED")]:
            with self.assertRaises(DeviceError) as caught:
                self.adapter(output).select()
            self.assertEqual(caught.exception.code, code)

    def test_explicit_target_and_missing_target(self):
        self.assertEqual(self.adapter("one\ntwo").select("two"), "two")
        with self.assertRaises(DeviceError):
            self.adapter("one").select("other")

    def test_error_text_is_not_a_device(self):
        with self.assertRaises(DeviceError):
            self.adapter("[Fail] device disconnected").devices()

    def test_install_exit_zero_is_not_enough(self):
        hdc = self.adapter("replace existing application")
        with self.assertRaises(DeviceError) as caught:
            hdc.install({"path": "app.hap"})
        self.assertEqual(caught.exception.code, "INSTALL_UNCONFIRMED")

    def test_install_uses_one_file_and_no_uninstall(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append(argv)
            return response("replace existing application" if argv[-1] == "-h" else "install bundle successfully.")
        hdc = Hdc(sys.executable, runner=runner)
        hdc.device = "chosen"
        self.assertEqual(hdc.install({"path": "a space/app.hap"})["status"], "passed")
        self.assertEqual(calls[-1][-3:], ["install", "-r", "a space/app.hap"])
        self.assertTrue(all("uninstall" not in call for call in calls))

    def test_launch_rejects_remote_shell_metacharacters(self):
        with self.assertRaises(DeviceError):
            self.adapter("start ability successfully").launch("app;reboot", "EntryAbility", "entry")

    def test_launch_failure_with_zero_exit_is_failure(self):
        with self.assertRaises(DeviceError):
            self.adapter("error: ability not found").launch("com.example.app", "Missing", "entry")

    def test_empty_pid_is_not_process_success(self):
        self.assertEqual(self.adapter("").pids("com.example.app"), [])
        with self.assertRaises(DeviceError):
            self.adapter("device disconnected").pids("com.example.app")


class DiagnosticTests(unittest.TestCase):
    def test_auth_uses_verdict_not_internal_code(self):
        reply = '1 12 12 D A/app/OHMapSDK_getMapPermission: request result: {"errCode":0,"code":6}'
        self.assertEqual(map_authorization([reply])["status"], "not-observed")
        good = '1 12 12 I A/app/OHMapSDK_MapComponent: checkMapPermission:true'
        bad = '1 12 12 I A/app/OHMapSDK_Mapview: checkMapPermission:false'
        self.assertEqual(map_authorization([reply, good])["status"], "passed")
        self.assertEqual(map_authorization([bad])["status"], "failed")
        self.assertEqual(map_authorization([good, bad])["status"], "mixed")
        self.assertEqual(map_authorization([good.replace('OHMapSDK_MapComponent', 'UserText')])["status"], "not-observed")

    def test_signature_mismatch_never_uninstalls(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append(argv)
            return response('replace existing application' if argv[-1] == '-h' else
                            'code:9568332 error: install sign info inconsistent.')
        with self.assertRaises(DeviceError) as caught:
            Hdc(sys.executable, runner=runner).install({'path': 'app.hap'})
        self.assertEqual(caught.exception.code, 'INSTALL_SIGNATURE_MISMATCH')
        self.assertEqual(len(calls), 2)
        self.assertFalse(any('uninstall' in c for c in calls))

    def test_launch_capture_does_not_install(self):
        with tempfile.TemporaryDirectory() as tmp, patch('ark_device.cli.Hdc') as adapter, \
                patch('ark_device.cli.capture_session') as capture, \
                patch('ark_device.cli.save_report', return_value='{}'), contextlib.redirect_stdout(io.StringIO()):
            def collect(hdc, bundle, seconds, limit, directory, result, launch):
                launch()
            capture.side_effect = collect
            code = main(['launch', '--capture', '--bundle', 'com.example.app', '--ability',
                         'EntryAbility', '--module', 'entry', '--output', str(Path(tmp) / 'out')])
            self.assertEqual(code, 0)
            adapter.return_value.install.assert_not_called()
            adapter.return_value.launch.assert_called_once_with('com.example.app', 'EntryAbility', 'entry')
            capture.assert_called_once()


class ProcessTests(unittest.TestCase):
    def test_success_captures_output_and_nonzero(self):
        result = execute([sys.executable, "-c", "print('diagnostic');raise SystemExit(7)"])
        self.assertEqual(result["exit_code"], 7)
        self.assertIn("diagnostic", result["output"])

    def test_timeout_is_bounded(self):
        started = time.monotonic()
        result = execute([sys.executable, "-c", "import time;time.sleep(30)"], timeout=.1)
        self.assertTrue(result["timed_out"])
        self.assertLess(time.monotonic() - started, 5)

    def test_flood_stops_at_limit(self):
        result = execute([sys.executable, "-c", "import sys;sys.stdout.write('x'*1000000)"], limit=1024)
        self.assertTrue(result["truncated"])
        self.assertEqual(len(result["output"]), 1024)


class CancellationTests(unittest.TestCase):
    def test_cancel_retains_output_and_stops_real_child(self):
        captures = []
        def create(argv, limit, **kwargs):
            capture = Capture(argv, limit, **kwargs)
            captures.append(capture)
            original = capture.process.wait
            calls = 0
            def wait(timeout=None):
                nonlocal calls
                calls += 1
                if calls == 1:
                    deadline = time.monotonic() + 3
                    while b'ready' not in capture.data and time.monotonic() < deadline:
                        time.sleep(.01)
                    raise KeyboardInterrupt()
                return original(timeout=timeout)
            capture.process.wait = wait
            return capture
        with patch('ark_device.process.Capture', side_effect=create), self.assertRaises(CommandCancelled) as caught:
            execute([sys.executable, '-c', "import time;print('ready',flush=True);time.sleep(30)"])
        self.assertIn('ready', caught.exception.evidence['output'])
        self.assertIsNotNone(captures[0].process.poll())
        self.assertFalse(captures[0].reader.is_alive())

    def test_hdc_keeps_cancelled_command_evidence(self):
        evidence = response('partial install progress')
        def runner(*args, **kwargs):
            raise CommandCancelled(evidence)
        hdc = Hdc(sys.executable, runner=runner)
        with self.assertRaises(CommandCancelled):
            hdc.call(['install', '-r', 'app.hap'])
        self.assertEqual(hdc.evidence, [evidence])


class SessionTests(unittest.TestCase):
    def test_immediate_limit_and_changed_pid_have_consistent_failure_stages(self):
        for early_limit in [True, False]:
            with self.subTest(early_limit=early_limit), tempfile.TemporaryDirectory() as tmp:
                hdc = Mock(device='synthetic')
                hdc.call.return_value = '1000000000'
                hdc.pids.side_effect = [['123'], ['123'], ['456']]
                capture = Mock(truncated=early_limit)
                capture.process.poll.return_value = 0 if early_limit else None
                capture.finish.return_value = '1000000001.0 123 123 I A/tag ready'
                result = {}
                with patch('ark_device.session.Capture', return_value=capture), patch('ark_device.session.time.sleep'):
                    with self.assertRaises(DeviceError) as caught:
                        capture_session(hdc, 'com.example.app', .001, 1024, Path(tmp), result)
                self.assertEqual(caught.exception.code, 'LOG_LIMIT' if early_limit else 'PROCESS_CHANGED')
                self.assertEqual(result['logs']['status'], 'failed')
                if not early_limit:
                    self.assertEqual(result['process_observation']['status'], 'failed')

    def test_capture_coverage_does_not_upgrade_missing_or_failed_evidence(self):
        complete = {'status': 'passed', 'lines': 10, 'truncated': False, 'device_dropped_lines_observed': 0}
        self.assertEqual(capture_coverage(complete), 'bounded-window')
        for change in [{'status': 'failed'}, {'status': 'cancelled'}, {'truncated': True},
                       {'device_dropped_lines_observed': 3}]:
            with self.subTest(change=change):
                self.assertEqual(capture_coverage(complete | change), 'partial')
        self.assertEqual(capture_coverage({}), 'not-run')
        self.assertEqual(capture_coverage({'status': 'passed', 'lines': 10, 'truncated': False}), 'unknown')
        self.assertEqual(capture_coverage(complete | {'lines': 0}), 'unknown')

    def test_report_separates_sdk_failure_from_operation_and_business(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = {'status': 'passed', 'install': {'status': 'passed'},
                      'business_acceptance': 'not-run',
                      'logs': {'status': 'passed', 'lines': 5, 'truncated': False, 'device_dropped_lines_observed': 2},
                      'diagnostics': {'error_level_lines': 1, 'map_authorization': {'status': 'failed'}}}
            saved = json.loads(save_report(Path(tmp), result, [], None))
            self.assertEqual(saved['status'], 'passed')
            self.assertEqual(saved['logs']['coverage'], 'partial')
            self.assertEqual(saved['business_acceptance'], 'not-run')
            report = (Path(tmp) / 'report.md').read_text()
            for heading in ['## Execution', '## Log capture', '## SDK and log signals', '## Business acceptance']:
                self.assertIn(heading, report)
            self.assertIn('Map authorization: failed', report)
            self.assertIn('Device dropped lines observed | 2', report)

    def test_filter_excludes_history_and_other_processes(self):
        text = "99.9 12 12 E A/tag old\n101.0 13 13 E A/tag other\n101.1 12 12 I A/tag ready"
        self.assertEqual(select_logs(text, {"12"}, 100), ["101.1 12 12 I A/tag ready"])

    def test_redaction(self):
        text = redact('password=secret token:abc device-123', 'device-123')
        self.assertNotIn('secret', text)
        self.assertNotIn('abc', text)
        self.assertNotIn('device-123', text)

    def test_redacted_summary_remains_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = save_report(Path(tmp), {"diagnostics": {"excerpt": 'message="quoted" token:abc'},
                                          "status": "failed"}, [], "device-one")
            data = json.loads(text)
            self.assertEqual(data["status"], "failed")
            self.assertNotIn("abc", text)
            self.assertIn("quoted", data["diagnostics"]["excerpt"])

    def run_session(self, mode="ok"):
        class FakeHdc:
            device = "test"
            def call(self, args):
                return str(int(time.time()))
            def pids(self, bundle):
                return ["123"]
            def argv(self, args):
                script = "import time;print(str(time.time())+' 123 123 I A/app ready',flush=True);time.sleep(10)"
                if mode == "disconnect":
                    script = "print('[Fail] device disconnected')"
                if mode == "empty":
                    script = "import time;time.sleep(10)"
                if mode == "drops":
                    script = "import time;print(str(time.time())+' 123 123 W A/app/HiLog: write socket failed, 7 line(s) dropped!',flush=True);time.sleep(10)"
                return [sys.executable, "-c", script]
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__('shutil').rmtree(directory))
        result = {}
        captures = []
        def tracked(argv, limit):
            item = Capture(argv, limit)
            captures.append(item)
            return item
        with patch('ark_device.session.Capture', side_effect=tracked):
            try:
                if mode == "cancel":
                    def launch():
                        raise KeyboardInterrupt()
                else:
                    launch = lambda: {"status": "passed"}
                capture_session(FakeHdc(), "com.example.app", .1, 10000, directory, result, launch)
            finally:
                self.assertTrue(all(c.process.poll() is not None and not c.reader.is_alive() for c in captures))
                if mode == 'cancel':
                    self.assertEqual(result['logs']['status'], 'cancelled')
        return result, directory

    def test_stream_success_and_cleanup(self):
        result, directory = self.run_session()
        self.assertEqual(result['logs']['status'], 'passed')
        self.assertIn('ready', (directory / 'target.log').read_text())
        self.assertFalse((directory / 'app-stream.log').exists())

    def test_device_loss_is_reported_without_claiming_collector_failure(self):
        result, directory = self.run_session('drops')
        self.assertEqual(result['logs']['status'], 'passed')
        self.assertEqual(result['logs']['device_dropped_lines_observed'], 7)
        self.assertEqual(capture_coverage(result['logs']), 'partial')

    def test_disconnect_does_not_pass(self):
        with self.assertRaises(DeviceError):
            self.run_session('disconnect')

    def test_zero_logs_does_not_pass(self):
        with self.assertRaises(DeviceError) as caught:
            self.run_session('empty')
        self.assertEqual(caught.exception.code, 'NO_TARGET_LOGS')

    def test_limit_reached_during_shutdown_cannot_pass(self):
        class FakeHdc:
            device = "test"
            def call(self, args):
                return "1000000000"
            def pids(self, bundle):
                return ["123"]
            def argv(self, args):
                return ["fake"]
        class LateLimit:
            truncated = False
            class process:
                @staticmethod
                def poll():
                    return None
            def finish(self):
                self.truncated = True
                return "1000000001.0 123 123 I A/tag ready"
        with tempfile.TemporaryDirectory() as tmp, patch('ark_device.session.Capture', return_value=LateLimit()):
            result = {}
            with self.assertRaises(DeviceError) as caught:
                capture_session(FakeHdc(), "com.example.app", .01, 1024, Path(tmp), result)
            self.assertEqual(caught.exception.code, "LOG_LIMIT")
            self.assertEqual(result["logs"]["status"], "failed")

    def test_cancellation_stops_collector(self):
        with self.assertRaises(KeyboardInterrupt):
            self.run_session('cancel')


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.hap = self.root / 'app.hap'
        with zipfile.ZipFile(self.hap, 'w') as z:
            z.writestr('module.json', json.dumps({'app': {'bundleName': 'com.example.app'},
                'module': {'name': 'entry', 'abilities': [{'name': 'EntryAbility'}]}}))

    def test_hap_hash_and_metadata(self):
        info = inspect_hap(self.hap)
        self.assertEqual(info['bundle'], 'com.example.app')
        self.assertEqual(len(info['sha256']), 64)
        self.assertIn('not locally verified', info['signature'])

    def test_target_mismatch_prevents_any_hdc_operation(self):
        out = self.root / 'evidence'
        with patch('ark_device.cli.Hdc') as tool, contextlib.redirect_stdout(io.StringIO()):
            code = main(['run', '--hap', str(self.hap), '--bundle', 'com.other.app',
                         '--ability', 'EntryAbility', '--module', 'entry', '--output', str(out)])
        tool.assert_not_called()
        self.assertEqual(code, 1)
        self.assertEqual(json.loads((out / 'report.json').read_text())['error']['code'], 'TARGET_MISMATCH')

    def test_cancelled_install_report_retains_stage_and_no_launch(self):
        out = self.root / 'cancelled'
        evidence = response('transfer in progress')
        with patch('ark_device.cli.Hdc') as adapter, contextlib.redirect_stdout(io.StringIO()):
            hdc = adapter.return_value
            hdc.device = 'synthetic'
            hdc.select.return_value = 'synthetic'
            hdc.evidence = [evidence]
            hdc.call.return_value = 'test version'
            hdc.install.side_effect = CommandCancelled(evidence)
            code = main(['run', '--hap', str(self.hap), '--bundle', 'com.example.app',
                         '--ability', 'EntryAbility', '--module', 'entry', '--output', str(out)])
            hdc.launch.assert_not_called()
        data = json.loads((out / 'report.json').read_text(encoding='utf-8'))
        self.assertEqual(code, 130)
        self.assertEqual(data['install']['status'], 'cancelled')
        self.assertEqual(data['commands'][0]['output'], 'transfer in progress')
        self.assertTrue((out / 'report.md').exists())

    def test_existing_output_directory_is_untouched(self):
        before = set(self.root.iterdir())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['doctor', '--output', str(self.root)]), 1)
        self.assertEqual(before, set(self.root.iterdir()))

    def test_missing_tool_returns_error_report(self):
        out = self.root / 'evidence'
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(['doctor', '--hdc', 'nonexistent-ark-hdc', '--output', str(out)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads((out / 'report.json').read_text())['error']['code'], 'HDC_MISSING')

    def test_invalid_duration_rejected_before_work(self):
        for value in ('0', '-1', 'nan', 'inf', '601'):
            with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(['logs', 'capture', '--bundle', 'com.example.app', '--seconds', value])


if __name__ == '__main__':
    unittest.main()
