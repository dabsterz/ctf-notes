"""Behavior checks for the real-input helpers, including wrong-assumption inputs."""
import base64
import importlib.util
import io
import json
from pathlib import Path
import struct
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'recipes'/f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class Recipes(unittest.TestCase):
    def test_rsa_supplied_ciphertext_known_and_close_factors(self):
        rsa = module('rsa')
        self.assertEqual(b'A', rsa.recover(dict(n=3233, e=17, c=2790, p=61, q=53))[2])
        p, q = 32416190071, 32416187567
        plain = b'new_RSA'
        m = int.from_bytes(plain, 'big')
        data = dict(n=p*q, e=65537, c=pow(m, 65537, p*q))
        self.assertEqual(plain, rsa.recover(data)[2])
        self.assertEqual(b'\0'+plain, rsa.recover(data | {'length':8})[2])
        with self.assertRaisesRegex(ValueError, 'budget'):
            rsa.recover(dict(n=3*1000000007, e=65537, c=1), steps=1)
        with self.assertRaisesRegex(ValueError, 'distinct'):
            rsa.recover(dict(n=3233, e=17, c=2790, p=2, q=3))

    def test_layers_plain_compressed_trailing_and_invalid(self):
        layers = module('layers')
        compressed = zlib.compress(b'new layer')
        self.assertEqual((compressed, b'new layer', b''), layers.decode(base64.b64encode(compressed)))
        self.assertEqual(b'extra', layers.decode(base64.b64encode(compressed+b'extra'))[2])
        self.assertEqual((b'plain', None, b''), layers.decode(b'cGxhaW4='))
        with self.assertRaises(ValueError): layers.decode(b'not%base64')
        with self.assertRaisesRegex(ValueError, 'truncated'): layers.decode(base64.b64encode(compressed[:-2]))
        with self.assertRaisesRegex(ValueError, 'budget'): layers.decode(base64.b64encode(zlib.compress(b'x'*1000)), limit=100)

    def test_transform_exact_order_non_ascii_and_empty_key(self):
        transform = module('transform')
        self.assertEqual(b'ABC', transform.invert(dict(key_hex='6b6579', rotation=3, expected=[81,57,209])))
        # A non-ASCII byte must survive; no text decoding is assumed.
        self.assertEqual(b'\xff', transform.invert(dict(key_hex='00', rotation=0, expected=[255])))
        with self.assertRaisesRegex(ValueError, 'key'): transform.invert(dict(key_hex='', rotation=3, expected=[1]))

    def test_vm_all_comparisons_reset_and_reject_unknown(self):
        vm = module('vm_byte')
        program = [['LOAD_INPUT'], ['XOR',35], ['ADD',7], ['CMP',111], ['HALT']]
        vm.validate(program)
        self.assertEqual([75], [v for v in range(256) if vm.run(program,v)[0]])
        contradictory = program[:-1] + [['CMP',112], ['HALT']]
        self.assertFalse(any(vm.run(contradictory,v)[0] for v in range(256)))
        with self.assertRaisesRegex(ValueError, 'unsupported'):
            vm.validate([['LOAD_INPUT'],['JUMP',1],['HALT']])
        with self.assertRaisesRegex(ValueError, 'CMP'):
            vm.validate([['LOAD_INPUT'],['XOR',2],['HALT']])

    def test_jwt_changes_payload_not_signature(self):
        jwt = module('jwt_claim')
        payload = base64.urlsafe_b64encode(b'{"role":"user","sub":"42"}').rstrip(b'=').decode()
        edited = jwt.mutate('header.'+payload+'.original', 'role', '"admin"')
        h, p, s = edited.split('.')
        self.assertEqual(('header','original'), (h,s))
        self.assertEqual({'role':'admin','sub':'42'}, json.loads(base64.urlsafe_b64decode(p+'='*(-len(p)%4))))
        with self.assertRaises(ValueError): jwt.mutate('not-a-jwt', 'role', '"admin"')

    def test_png_chunk_boundary_not_embedded_iend(self):
        png = module('png_tail')
        def chunk(kind, body):
            return struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body))
        data = b'\x89PNG\r\n\x1a\n'+chunk(b'tEXt',b'fake IEND marker')+chunk(b'IEND',b'')+b'real trailer'
        tail, checks = png.inspect(data)
        self.assertEqual(b'real trailer', tail)
        self.assertTrue(all(c[2] for c in checks))
        with self.assertRaisesRegex(ValueError, 'signature'): png.inspect(b'not png')
        with self.assertRaisesRegex(ValueError, 'beyond'): png.inspect(data[:20])

    def test_tar_cli_keeps_duplicates_and_refuses_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            archive = folder/'input.tar'
            with tarfile.open(archive,'w') as tf:
                for value in (b'old answer',b'new decoy'):
                    info = tarfile.TarInfo('../../same.txt')
                    info.size = len(value)
                    tf.addfile(info,io.BytesIO(value))
            cmd = [sys.executable,str(ROOT/'recipes/tar_keep.py'),str(archive),'--out',str(folder/'parts')]
            result = subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertEqual(b'old answer',(folder/'parts/000000.bin').read_bytes())
            self.assertEqual(b'new decoy',(folder/'parts/000001.bin').read_bytes())
            entries = [json.loads(x) for x in (folder/'parts/manifest.jsonl').read_text().splitlines()]
            self.assertEqual(['../../same.txt']*2,[e['name'] for e in entries])
            self.assertNotEqual(0,subprocess.run(cmd,capture_output=True).returncode)

    def test_pattern_command_matches_documented_offset(self):
        cmd = [sys.executable,str(ROOT/'recipes/pattern.py'),'--find','61616763']
        result = subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr)
        self.assertEqual('173',result.stdout.strip())
        self.assertNotEqual(0,subprocess.run(cmd[:-1]+['1234'],capture_output=True).returncode)

    def test_pattern_verifies_bytes_in_actually_sent_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            script=str(ROOT/'recipes/pattern.py')
            subprocess.run([sys.executable,script,'--length','512'],cwd=tmp,check=True,capture_output=True)
            cmd=[sys.executable,script,'--find','61616763','--sent','pattern.bin']
            result=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True)
            self.assertEqual(0,result.returncode,result.stderr)
            self.assertIn('verified against sent file',result.stdout)
            (Path(tmp)/'pattern.bin').write_bytes(b'wrong generator')
            self.assertNotEqual(0,subprocess.run(cmd,cwd=tmp,capture_output=True).returncode)

    def test_every_recipe_has_runnable_help(self):
        for script in (ROOT/'recipes').glob('*.py'):
            with self.subTest(script=script.name):
                result = subprocess.run([sys.executable,str(script),'--help'],capture_output=True,text=True)
                self.assertEqual(0,result.returncode,result.stderr)


if __name__ == '__main__':
    unittest.main()
