"""目录换版后旧来源仍留在当前范围的基线行为。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.collection import collect,coverage
from capture_service.view import overview

ROOT=Path(__file__).resolve().parents[1]

class ScopeChange(unittest.TestCase):
    def test_catalog_replacement_currently_keeps_old_source(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'state.sqlite3')
            collect(c,'sample',ROOT/'data'/'normal.json')
            collect(c,'sample',ROOT/'data'/'scope-change.json')
            state=coverage(c,'sample')
            self.assertEqual(state['expected'],3)
            self.assertEqual(state['received'],2)
            self.assertTrue(overview(c,'sample')['publishable'])
            c.close()
