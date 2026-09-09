"""Check actual distribution resources and entrypoint discoverability."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_nine_unique_entrypoints(self):
        paths = [ROOT / "SKILL.md", *sorted(ROOT.glob("ark-*/SKILL.md"))]
        names = []
        for path in paths:
            text = path.read_text(encoding="utf-8-sig")
            match = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---", text)
            self.assertIsNotNone(match, path)
            names.append(match[1])
        self.assertEqual(set(names), {"ark", "ark-scan", "ark-language", "ark-ui", "ark-flow", "ark-kit", "ark-native", "ark-test", "ark-check"})
        self.assertEqual(len(names), len(set(names)))

    def test_linked_local_resources_exist_and_stay_in_package(self):
        files = [ROOT / "SKILL.md", ROOT / "README.md", *ROOT.glob("ark-*/SKILL.md"), *ROOT.glob("references/*.md"), ROOT / "tests/skill-scenarios.md"]
        for path in files:
            text = path.read_text(encoding="utf-8-sig")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT), (path, link))
                self.assertTrue(target.exists(), (path, link))


if __name__ == "__main__":
    unittest.main()
