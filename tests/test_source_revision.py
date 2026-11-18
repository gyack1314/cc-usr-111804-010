"""来源晚到与修订保留各自收据，并不改写旧发布视图。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.collection import collect,coverage
from capture_service.archive import release,get
from capture_service.ledger import connect,entities

ROOT=Path(__file__).resolve().parents[1]
COLLECTION='111804-010'

class SourceRevision(unittest.TestCase):
    def test_staged_arrival_and_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'collection.sqlite3')
            collect(c,COLLECTION,ROOT/'data'/'partial.json')
            self.assertEqual(coverage(c,COLLECTION)['received'],1)
            old=release(c,COLLECTION)
            prior=get(c,COLLECTION,old)
            collect(c,COLLECTION,ROOT/'data'/'normal.json')
            self.assertEqual(coverage(c,COLLECTION)['received'],2)
            collect(c,COLLECTION,ROOT/'data'/'revised.json')
            self.assertEqual(len(entities(c,COLLECTION)),3)
            self.assertEqual(get(c,COLLECTION,old),prior)
            c.close()
