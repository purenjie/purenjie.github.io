"""Font delivery contracts: uv run --with 'fonttools[woff]==4.60.2' python scripts/test_subset_font.py."""
import hashlib
import json
import unittest

from fontTools.ttLib import TTFont
from fontTools.unicodedata import mirrored
from subset_font import ROOT, SOURCE, GROUPS, OUTPUT, CSS, parse_ranges, format_ranges, partition


class FontContracts(unittest.TestCase):
    def test_unlisted_and_supplementary_characters_are_preserved(self):
        available = {0x41, 0x4E00, 0x4E01, 0x9F98, 0x20000}
        config = {"groups": [{"id": "subset-1", "unicode_range": "U+41-42,U+4E00"}],
                  "remainder_chunk_size": 2}
        groups = partition(available, config)
        self.assertEqual(groups[0][1], {0x41, 0x4E00})
        self.assertEqual(set.union(*(chars for _, chars in groups)), available)
        self.assertEqual(sum(len(chars) for _, chars in groups), len(available))
        self.assertEqual(parse_ranges(format_ranges(available)), available)

    def test_overlapping_groups_fail(self):
        config = {"groups": [{"id": "subset-1", "unicode_range": "U+41-42"},
                             {"id": "subset-2", "unicode_range": "U+42"}],
                  "remainder_chunk_size": 2}
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            partition({0x41, 0x42}, config)

    def test_invalid_ranges_fail(self):
        for value in ["U+43-41", "U+110000", "41", "U+ZZZZ"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_ranges(value)

    def test_published_fonts_match_css_and_source(self):
        manifest = json.loads((OUTPUT / "manifest.json").read_text())
        self.assertEqual(manifest['source_sha256'], hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(manifest['grouping_sha256'], hashlib.sha256(GROUPS.read_bytes()).hexdigest())
        css = CSS.read_text()
        covered = set()
        with TTFont(SOURCE) as source:
            original = set(source.getBestCmap())
            copyright_names = {n.toUnicode() for n in source['name'].names if n.nameID == 0}
        for entry in manifest['subsets']:
            path = OUTPUT / entry['file']
            with TTFont(path) as font:
                actual = set(font.getBestCmap())
                declared = parse_ranges(entry['unicode_range'])
                self.assertEqual(actual, declared | ({mirrored(cp) for cp in declared} & original))
                self.assertFalse(covered & declared)
                self.assertEqual(font['OS/2'].usWeightClass, 400)
                self.assertTrue(copyright_names <= {n.toUnicode() for n in font['name'].names if n.nameID == 0})
            covered.update(declared)
            self.assertEqual(path.stat().st_size, entry['bytes'])
            self.assertIn(hashlib.sha256(path.read_bytes()).hexdigest()[:16], path.name)
            self.assertIn(f"/fonts/jinkai/{path.name}", css)
            self.assertIn(f"unicode-range: {entry['unicode_range']};", css)
        self.assertEqual(covered, original)
        self.assertEqual(css.count('font-display: swap;'), len(manifest['subsets']))
        self.assertNotIn('/fonts/cang-er-jin-kai.woff2', css)
        self.assertNotIn('/fonts/cang-er-jin-kai.woff2', (ROOT / 'src/components/BaseHead.astro').read_text())


if __name__ == '__main__':
    unittest.main()
