"""Checks for the generated, offline human handbook."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BuilderContract(unittest.TestCase):
    def builder(self):
        path = ROOT / "build.py"
        self.assertTrue(path.exists(), "The offline handbook builder is not implemented")
        spec = importlib.util.spec_from_file_location("handbook_builder", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_payloads_are_displayed_not_executed(self):
        module = self.builder()
        result = module.render_markdown("# Test\n\n```html\n<script>alert(1)</script>\n```\n", "test")
        self.assertIn("&lt;script&gt;", result)
        self.assertNotIn("<script>", result)

    def test_headings_have_stable_unique_chapter_scoped_ids(self):
        module = self.builder()
        result = module.render_markdown("# Test\n\n## Check\n\n## Check\n", "web")
        self.assertIn('id="web--check"', result)
        self.assertIn('id="web--check_1"', result)

    def test_untrusted_links_and_markup_are_inert(self):
        module = self.builder()
        result = module.render_markdown('<script>alert(1)</script>\n\n<a href="javascript:alert(1)" onclick="alert(2)">x</a>', "x")
        self.assertNotIn("<script", result)
        self.assertNotIn("onclick", result)
        self.assertNotIn("javascript:", result)

    def test_workbook_preserves_all_entries_and_platforms(self):
        module = self.builder()
        entries = module.load_tools()
        self.assertEqual(282, len(entries))
        self.assertEqual(39, sum(t["platform"] == "Windows / WSL" for t in entries))
        self.assertEqual(161, sum(t["platform"] == "Kali" for t in entries))
        self.assertEqual(82, sum(t["status"] == "Unapproved" for t in entries))
        r2 = next(t for t in entries if t["name"] == "radare2")
        self.assertEqual("C123", r2["cell"])
        self.assertEqual("Kali", r2["platform"])

    def test_merged_markdown_retains_recipe_level_destinations(self):
        module = self.builder()
        source = '# Topic\n\n## Recipe\n\n[other](other.md#step) [same](#recipe)\n\n```text\n## Not a heading\n```\n'
        result = module.merge_markdown(source, 'topic')
        self.assertIn('<a id="topic--recipe"></a>', result)
        self.assertIn('[other](#other--step)', result)
        self.assertIn('[same](#topic--recipe)', result)
        self.assertNotIn('id="topic--not-a-heading"', result)

    def test_table_markdown_escape_does_not_change_shell_command(self):
        module = self.builder()
        result = module.render_markdown("| Command |\n| --- |\n| `tool --only 'pop\\|ret'` |\n", 'tools')
        self.assertIn("tool --only 'pop|ret'", result)
        self.assertNotIn('pop\\|ret', result)


if __name__ == "__main__":
    unittest.main()
