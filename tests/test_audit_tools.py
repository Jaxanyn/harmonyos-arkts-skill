"""Regression tests using disposable synthetic projects, never user data."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import audit_harmony_project as project
import check_skill_privacy as privacy


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
        return file

    def test_nested_modules_and_test_source_sets(self):
        self.put("apps/client/src/main/module.json5", '{module: {name: "client", type: "entry"}}')
        self.put("libs/shared/src/main/module.json5", "{module: {name: 'shared', type: 'shared'}}")
        self.put("apps/client/src/ohosTest/module.json5", '{module: {type: "entry"}}')
        report = project.build_report(self.root)["summary"]
        self.assertEqual(report["modules"], ["apps/client", "libs/shared"])
        self.assertEqual(report["libraryBoundaryCandidates"], ["libs/shared/src/main/module.json5"])

    def test_bom_json5_comments_and_numeric_sdk(self):
        self.put("build-profile.json5", '\ufeff{ // targetSdkVersion: 999\n targetSdkVersion: 19, compatibleSdkVersion: "5.1.1(19)", /* compileSdkVersion: 100 */ }')
        signals = project.build_report(self.root)["signals"]
        self.assertEqual(signals["sdkVersions"], ["19", "5.1.1(19)"])
        self.assertEqual({item["field"] for item in signals["sdkFields"]}, {"targetSdkVersion", "compatibleSdkVersion"})

    def test_comments_preserve_strings(self):
        content = '{ url: "https://example.invalid/a", text: "/* literal */", /* noise */ type: "har" }'
        clean = project.strip_comments(content)
        self.assertIn('https://example.invalid/a', clean)
        self.assertIn('/* literal */', clean)
        self.assertNotIn('noise', clean)
        self.assertEqual(project.field_values(content, "type"), ["har"])

    def test_cmake_only_project_routes_native(self):
        self.put("native/CMakeLists.txt", "add_library(engine SHARED engine.cpp)")
        self.assertIn("$ark-native", project.build_report(self.root)["signals"]["suggestedRoutes"])

    def test_declarations_alone_do_not_prove_native(self):
        self.put("types/index.d.ts", "export interface Result { value: number }")
        self.assertNotIn("$ark-native", project.build_report(self.root)["signals"]["suggestedRoutes"])

    def test_generated_trees_and_readme_do_not_supply_platform_facts(self):
        self.put("build/fake.ets", "@ComponentV2 struct Wrong {}")
        self.put("node_modules/fake.cpp", "void example() {}")
        self.put("README.md", "import x from '@kit.FakeKit'; napi_example();")
        self.put("src/main.ets", "// @ComponentV2\n@Component struct Page { @State n: number = 0; }")
        report = project.build_report(self.root)
        self.assertEqual(report["summary"]["etsFiles"], 1)
        self.assertEqual(report["signals"]["kitImports"], [])
        self.assertNotIn("$ark-native", report["signals"]["suggestedRoutes"])
        self.assertEqual(report["signals"]["stateManagement"][0]["markers"], ["Component", "State"])

    def test_v1_v2_are_per_file_and_fa_is_only_a_candidate(self):
        self.put("old.ets", "@Component struct Old { @State n: number = 0; }")
        self.put("new.ets", "@ComponentV2 struct New { @Local n: number = 0; }")
        self.put("legacy/config.json", '{"module": {"abilities": []}}')
        signals = project.build_report(self.root)["signals"]
        self.assertEqual(len(signals["stateManagement"]), 2)
        self.assertEqual(signals["modelEvidence"]["faCandidates"], ["legacy/config.json"])
        self.assertEqual(signals["modelEvidence"]["stage"], [])

    def test_large_and_invalid_text_are_reported(self):
        self.put("large.ets", " " * (project.MAX_TEXT_BYTES + 1))
        bad = self.put("invalid.ets", "")
        bad.write_bytes(b"\xff\xfe\xfd")
        report = project.build_report(self.root)
        self.assertEqual({item["path"] for item in report["warnings"]}, {"large.ets", "invalid.ets"})

    def test_signing_values_never_enter_report(self):
        sentinel = "synthetic-sensitive-value-123"
        self.put("build-profile.json5", json.dumps({"signingConfigs": [{"keyPassword": sentinel}]}))
        report = project.build_report(self.root)
        self.assertIn("signing config", report["signals"]["protectedSurfaces"])
        self.assertNotIn(sentinel, json.dumps(report))

    def test_paths_under_parent_named_build_are_not_all_ignored(self):
        self.put("build/project/src/page.ets", "@Component struct Page {}")
        self.assertEqual(project.build_report(self.root / "build/project")["summary"]["etsFiles"], 1)

    def test_symlink_not_followed(self):
        target = self.put("outside/data.ets", "@Component struct Private {}")
        selected = self.root / "selected"
        selected.mkdir()
        try:
            (selected / "linked.ets").symlink_to(target)
        except OSError:
            self.skipTest("Host cannot create symlinks")
        self.assertEqual(project.build_report(selected)["summary"]["etsFiles"], 0)

    def test_privacy_findings_are_redacted_and_domain_neutral(self):
        sentinel = "synthetic-sensitive-value-456"
        self.put("config.json", json.dumps({"password": sentinel}))
        findings = privacy.scan(self.root, [])
        self.assertTrue(findings)
        self.assertNotIn(sentinel, repr(findings))
        self.assertEqual(privacy.DEFAULT_TERMS, [])

    def test_custom_term_not_echoed(self):
        term = "private-customer-fixture"
        self.put("note.md", term)
        findings = privacy.scan(self.root, [term])
        self.assertTrue(findings)
        self.assertNotIn(term, repr(findings))

    def test_privacy_unreadable_content_cannot_pass(self):
        bad = self.put("invalid.md", "")
        bad.write_bytes(b"\xff\xfe\xfd")
        with patch.object(sys, "argv", ["check_skill_privacy.py", str(self.root)]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(privacy.main(), 2)

    def test_scan_does_not_modify_project(self):
        source = self.put("entry/src/main/module.json5", '{module: {type: "entry"}}')
        before = source.read_bytes()
        paths = list(self.root.rglob("*"))
        project.build_report(self.root)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(list(self.root.rglob("*")), paths)


if __name__ == "__main__":
    unittest.main()
