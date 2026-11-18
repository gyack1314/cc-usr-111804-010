"""来源目录先到、正文后到时，覆盖状态沿采集和视图变化。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.collection import collect, coverage
from capture_service.ledger import connect
from capture_service.archive import release, get

ROOT = Path(__file__).resolve().parents[1]

class PartialCoverage(unittest.TestCase):
    def test_late_source_does_not_rewrite_old_release(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / 'sources.sqlite3'
            connection = connect(database)
            collect(connection, '111804-010', ROOT / 'data' / 'partial.json')
            pending = coverage(connection, '111804-010')
            self.assertEqual(pending['expected'], 2)
            self.assertEqual(pending['received'], 1)
            self.assertEqual(len(pending['missing_required']), 1)
            version = release(connection, '111804-010')
            previous = get(connection, '111804-010', version)
            connection.close()
            connection = connect(database)
            collect(connection, '111804-010', ROOT / 'data' / 'normal.json')
            self.assertEqual(coverage(connection, '111804-010')['received'], 2)
            self.assertEqual(get(connection, '111804-010', version), previous)
            connection.close()
