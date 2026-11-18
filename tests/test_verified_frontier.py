"""A transport receipt does not by itself close the business source frontier."""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.collection import collect,coverage
from capture_service.archive import release_verified

ROOT=Path(__file__).resolve().parents[1]

class VerifiedFrontier(unittest.TestCase):
    def test_partial_then_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'state.sqlite3')
            collect(c,'sample',ROOT/'data'/'partial.json')
            self.assertEqual(len(coverage(c,'sample')['unverified_required']),2)
            with self.assertRaises(ValueError):release_verified(c,'sample')
            collect(c,'sample',ROOT/'data'/'normal.json')
            self.assertEqual(coverage(c,'sample')['unverified_required'],[])
            release_verified(c,'sample')
            c.close()
