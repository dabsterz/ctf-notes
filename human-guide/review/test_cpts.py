import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class CPTSImportTests(unittest.TestCase):
    def test_ids_distinguish_same_title_in_different_folders(self):
        c = module('cpts_support')
        self.assertNotEqual(c.note_id('Linux/Checklist.md'), c.note_id('Windows/Checklist.md'))
        self.assertRegex(c.note_id('PrivEsc/$PATH.md'), r'^cpts-[a-z0-9-]+$')

    def test_conversion_leaves_shell_syntax_and_code_images_literal(self):
        c = module('cpts_support')
        source = ' ```bash\n[[ $GREP ]]\n[[:space:]]\n![[example.png]]\n```\n\n![[example.png]]\n'
        converted = c.convert_note(source, {'example.png': '../assets/example.png'})
        self.assertIn('```bash\n[[ $GREP ]]\n[[:space:]]\n![[example.png]]\n```', converted)
        self.assertIn('![example.png](../assets/example.png)', converted)

    def test_snapshot_preserves_raw_bytes_and_honors_explicit_exclusions(self):
        c = module('cpts_support')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); vault = base / 'Vault'; source = vault / 'CPTS'; dest = base / 'guide'
            source.mkdir(parents=True); (vault / 'Attachments').mkdir()
            raw = b'# Original\r\n\r\n![[shot.png]]\r\n'
            (source / 'Keep.md').write_bytes(raw); (source / 'Skip.md').write_text('excluded')
            image = b'\x89PNG\r\n\x1a\n' + b'test'
            (vault / 'Attachments/shot.png').write_bytes(image)
            manifest = c.import_vault(source, dest, {'Skip.md'})
            self.assertEqual(len(manifest['notes']), 1)
            self.assertEqual((dest / manifest['notes'][0]['file']).read_bytes(), raw)
            self.assertEqual((dest / manifest['assets'][0]['file']).read_bytes(), image)
            self.assertEqual(manifest['excluded'], ['Skip.md'])

    def test_malformed_language_label_keeps_multiline_commands_copyable(self):
        from bs4 import BeautifulSoup
        c = module('cpts_support'); b = module('build')
        source = '```cmd*****\nrunas first\nrunas second\n```\n'
        rendered = BeautifulSoup(b.render_markdown(c.convert_note(source, {}), 'test'), 'html.parser')
        block = rendered.select_one('pre code')
        self.assertIsNotNone(block)
        self.assertEqual(block.get_text(), 'runas first\nrunas second\n')

    def test_only_explicitly_supplied_images_render(self):
        b = module('build')
        uri = 'data:image/png;base64,' + base64.b64encode(b'\x89PNG\r\n\x1a\n').decode()
        html = b.render_markdown('![ok](../assets/ok.png)\n\n![remote](https://example.com/x.png)', 'cpts-test', images={'../assets/ok.png': uri})
        self.assertIn(uri, html)
        self.assertNotIn('https://example.com/x.png', html)
        self.assertEqual(html.count('<img '), 1)


if __name__ == '__main__':
    unittest.main()
