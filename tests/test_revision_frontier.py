"""来源目录指向同链接新版本时，当前基线尚未追踪版次。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.collection import collect,register_sources,coverage
from capture_service.archive import release_verified,get
from capture_service.view import overview

ROOT=Path(__file__).resolve().parents[1]

class RevisionFrontier(unittest.TestCase):
    def test_revision_notice_does_not_yet_change_current_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'state.sqlite3')
            collect(c,'sample',ROOT/'data'/'normal.json')
            old=release_verified(c,'sample')
            frozen=get(c,'sample',old)
            register_sources(c,'sample',ROOT/'data'/'revised.json')
            self.assertEqual(c.execute(
                'SELECT expected_revision FROM collection_sources WHERE collection=? AND source_kind=?',
                ('sample', 'interface_spec')).fetchone()[0], 'v2')
            self.assertEqual(coverage(c,'sample')['unverified_required'],[])
            self.assertTrue(overview(c,'sample')['publishable'])
            release_verified(c,'sample')
            self.assertEqual(get(c,'sample',old),frozen)
            c.close()
