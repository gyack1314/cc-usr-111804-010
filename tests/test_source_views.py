"""两种业务来源分别保留原文身份和来源指纹。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.collection import collect
from capture_service.ledger import connect
from capture_service.primary_records import current as primary
from capture_service.supporting_records import current as supporting
ROOT=Path(__file__).resolve().parents[1]
class SourceViews(unittest.TestCase):
    def test_initial_sources_remain_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            connection=connect(Path(directory)/'sources.sqlite3')
            collect(connection,'sample',ROOT/'data'/'normal.json')
            self.assertEqual(len(primary(connection,'sample')),1)
            self.assertEqual(len(supporting(connection,'sample')),1)
            self.assertNotEqual(primary(connection,'sample')[0]['source_sha256'],
                                supporting(connection,'sample')[0]['source_sha256'])
            connection.close()
