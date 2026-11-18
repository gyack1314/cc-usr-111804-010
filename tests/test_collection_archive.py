"""来源进度在重启后仍可接续，已发布视图保持原状。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.collection import collect, progress
from capture_service.archive import release, get

ROOT = Path(__file__).resolve().parents[1]

class CollectionArchive(unittest.TestCase):
    def test_receive_restart_and_release(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sources.sqlite3'
            connection = connect(path)
            receipts = collect(connection, '111804-010', ROOT / 'data' / 'normal.json')
            self.assertEqual(len(receipts), 2)
            original_revision = release(connection, '111804-010')
            original = get(connection, '111804-010', original_revision)
            connection.close()
            connection = connect(path)
            self.assertEqual(len(progress(connection, '111804-010')), 2)
            self.assertEqual(len(collect(connection, '111804-010', ROOT / 'data' / 'normal.json')), 2)
            self.assertEqual(len(progress(connection, '111804-010')), 2)
            self.assertEqual(get(connection, '111804-010', original_revision), original)
            connection.close()
