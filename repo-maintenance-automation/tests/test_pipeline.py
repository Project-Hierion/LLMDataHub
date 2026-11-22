#!/usr/bin/env python3
"""Offline regression rig for the harvester pipeline. No network, no GitHub.

Run:  python3 tests/test_pipeline.py
Exit: 0 = all green, 1 = failures.
"""

import re
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).resolve().parent.parent / "rma"
sys.path.insert(0, str(SRC))
FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"

import formatter  # noqa: E402
import classifier  # noqa: E402


PIPE_DESC = "A | B | C pipe separator test"
CTRL_DESC = "line1\nline2\ttabbed\x00null"


def structural_pipes(row: str) -> int:
    """Count unescaped (structural) pipes in a table row."""
    masked = re.sub(r"\\\|", "X", row)
    return masked.count("|")


class TestSanitizeCell(unittest.TestCase):
    def test_pipe_escaped(self):
        self.assertEqual(formatter.sanitize_cell(PIPE_DESC),
                         "A \\| B \\| C pipe separator test")

    def test_already_escaped_not_double_escaped(self):
        self.assertEqual(formatter.sanitize_cell("A \\| B"), "A \\| B")

    def test_control_chars_stripped(self):
        out = formatter.sanitize_cell(CTRL_DESC)
        self.assertNotIn("\n", out)
        self.assertNotIn("\x00", out)
        self.assertNotIn("\t", out)

    def test_none_and_empty(self):
        self.assertEqual(formatter.sanitize_cell(None), "")
        self.assertEqual(formatter.sanitize_cell(""), "")

    def test_whitespace_collapsed(self):
        self.assertEqual(formatter.sanitize_cell("  lots   of \t space  "),
                         "lots of space")


class TestRowBuilders(unittest.TestCase):
    def _ds_row(self, desc):
        return formatter.format_dataset_row({
            "name": "test-ds", "url": "https://github.com/o/test-ds",
            "description": desc, "stars": 5, "language": "Python",
        })

    def test_dataset_row_column_count(self):
        # 8 columns => 9 unescaped structural pipes
        self.assertEqual(structural_pipes(self._ds_row("plain")), 8)

    def test_dataset_row_pipes_in_description_survive(self):
        row = self._ds_row(PIPE_DESC)
        self.assertEqual(structural_pipes(row), 8)
        self.assertIn("A \\| B \\| C", row)

    def test_paper_row_no_lang_or_stars(self):
        row = formatter.format_paper_row({
            "name": "p", "url": "https://github.com/o/p",
            "description": "d",
        })
        self.assertIn("| Paper | — | — |", row)

    def test_untrusted_description_control_chars(self):
        row = formatter.format_tool_row({
            "name": "x", "url": "https://github.com/o/x",
            "description": CTRL_DESC, "stars": 2, "language": "Rust",
        })
        self.assertNotIn("\x00", row)
        self.assertNotIn("\n", row)


class TestYearSectionResolver(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def _write_fixture(self, name, divs):
        p = Path(self.tmp) / name
        p.write_text("\n".join(
            f'### <div id="{d}">{d.split("-")[1]}</div>\n' for d in divs
        ))
        return p

    def test_prefers_current_year(self):
        p = self._write_fixture("M.md", ["models-2024", "models-2026"])
        anchor = formatter._target_year_section(str(p), "models")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"models-2026"'), anchor)

    def test_falls_back_to_highest_year(self):
        # Simulated year 2027: 2027 div absent -> 2026 must win
        p = self._write_fixture("M.md", ["models-2024", "models-2026"])

        class FakeDT(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2027, 6, 1)

        with patch.object(formatter, "datetime", FakeDT):
            anchor = formatter._target_year_section(str(p), "models")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"models-2026"'), anchor)

    def test_new_year_wins_when_present(self):
        # 2027 div exists in file and it is 2027 -> 2027 wins
        p = self._write_fixture("M.md", ["models-2025", "models-2027"])

        class FakeDT(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime(2027, 6, 1)

        with patch.object(formatter, "datetime", FakeDT):
            anchor = formatter._target_year_section(str(p), "models")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"models-2027"'), anchor)

    def test_no_year_divs_returns_none(self):
        p = Path(self.tmp) / "empty.md"
        p.write_text("nothing here\n")
        self.assertIsNone(formatter._target_year_section(str(p), "models"))

    def test_missing_file_returns_none(self):
        self.assertIsNone(
            formatter._target_year_section(str(Path(self.tmp) / "nope.md"), "models")
        )

    def test_real_fixture_modes_md_resolves(self):
        anchor = formatter._target_year_section(str(FIXTURES / "MODELS.md"), "models")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"models-2026"'), anchor)

    def test_real_fixture_tools_md_resolves(self):
        anchor = formatter._target_year_section(str(FIXTURES / "TOOLS.md"), "tools")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"tools-2026"'), anchor)

    def test_real_fixture_papers_md_resolves(self):
        anchor = formatter._target_year_section(str(FIXTURES / "PAPERS.md"), "papers")
        self.assertIsNotNone(anchor)
        self.assertIn(re.escape('"papers-2026"'), anchor)


class TestInsertionAgainstRealFixture(unittest.TestCase):
    """Full end-to-end insertion on a copy of the live MODELS.md."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.models = Path(self.tmp) / "MODELS.md"
        shutil.copy(FIXTURES / "MODELS.md", self.models)

    def _anchor(self):
        return formatter._target_year_section(str(self.models), "models")

    def test_pipey_row_inserts_cleanly(self):
        rows = [
            formatter.format_model_row({
                "name": "pipe-hero",
                "url": "https://github.com/someone/pipe-hero",
                "description": PIPE_DESC,
                "stars": 42, "language": "Python",
            })
        ]
        self.assertTrue(formatter.insert_rows_into_file(str(self.models), self._anchor(), rows))
        content = self.models.read_text()
        self.assertIn("A \\| B \\| C", content)
        self.assertIn("[pipe-hero](https://github.com/someone/pipe-hero)", content)

    def test_inserted_row_has_same_structural_pipe_count_as_neighbors(self):
        rows = [
            formatter.format_model_row({
                "name": "pipe-hero",
                "url": "https://github.com/someone/pipe-hero",
                "description": PIPE_DESC,
                "stars": 42, "language": "Python",
            })
        ]
        self.assertTrue(formatter.insert_rows_into_file(str(self.models), self._anchor(), rows))
        lines = self.models.read_text().splitlines()
        inserted = [l for l in lines if "pipe-hero" in l][0]
        neighbors = [l for l in lines if l.strip().startswith("|")
                     and "pipe-hero" not in l and "---" not in l][:3]
        self.assertEqual(len(neighbors), 3)
        for nb in neighbors:
            self.assertEqual(structural_pipes(inserted), structural_pipes(nb))

    def test_dupes_skipped(self):
        # rf-detr already listed -> new row with same identifiers must be
        # skipped and the file must remain byte-identical.
        before = self.models.read_bytes()
        rows = [
            formatter.format_model_row({
                "name": "rf-detr",
                "url": "https://github.com/roboflow/rf-detr",
                "description": "Vision model", "stars": 100, "language": "Python",
            })
        ]
        self.assertTrue(formatter.insert_rows_into_file(str(self.models), self._anchor(), rows))
        self.assertEqual(self.models.read_bytes(), before)


class TestClassifierSmoke(unittest.TestCase):
    def test_classify_known_shape(self):
        cand = {
            "name": "foo-datasets",
            "full_name": "someone/foo-datasets",
            "description": "A collection of QA pairs benchmark corpus",
            "topics": [],
        }
        cat, score = classifier.classify_repo(cand)
        self.assertEqual(cat, "dataset")
        self.assertGreaterEqual(score, 0.75)

    def test_corporate_blocked(self):
        cand = {
            "name": "foo",
            "full_name": "openai/foo",
            "description": "A dataset of QA pairs benchmark corpus",
            "topics": [],
        }
        cat, _ = classifier.classify_repo(cand)
        self.assertEqual(cat, "corporate")


if __name__ == "__main__":
    unittest.main(verbosity=2)
