"""初版双来源业务关联可以通过现有采集与发布操作读取。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.collection import collect
from capture_service.view import overview
from capture_service.archive import release_verified,get

ROOT=Path(__file__).resolve().parents[1]
COLLECTION='111804-010'

class InitialBusinessFlow(unittest.TestCase):
    def test_pair_is_verifiable_and_releasable(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'service.sqlite3')
            collect(c,COLLECTION,ROOT/'data'/'normal.json')
            state=overview(c,COLLECTION)
            self.assertTrue(state['publishable'])
            self.assertEqual(len(state['matched_pairs']),1)
            self.assertFalse(state['coverage']['missing_required'])
            revision=release_verified(c,COLLECTION)
            self.assertEqual(get(c,COLLECTION,revision),state)
            c.close()
