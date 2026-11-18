"""第三种来源进入目录后，采集覆盖与来源版次可接续。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.collection import collect,coverage
from capture_service.ledger import connect,entities
from capture_service.archive import release,get

ROOT=Path(__file__).resolve().parents[1]
COLLECTION='111804-010'

class BusinessEvent(unittest.TestCase):
    def test_third_source_arrives_after_prior_release(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'collection.sqlite3')
            collect(c,COLLECTION,ROOT/'data'/'normal.json')
            original=release(c,COLLECTION)
            before=get(c,COLLECTION,original)
            collect(c,COLLECTION,ROOT/'data'/'event-pending.json')
            pending=coverage(c,COLLECTION)
            self.assertEqual(pending['expected'],3)
            self.assertEqual(pending['received'],2)
            self.assertEqual(len(pending['missing_required']),1)
            collect(c,COLLECTION,ROOT/'data'/'event-complete.json')
            complete=coverage(c,COLLECTION)
            self.assertEqual(complete['received'],3)
            self.assertFalse(complete['missing_required'])
            self.assertEqual(len(entities(c,COLLECTION)),3)
            self.assertEqual(get(c,COLLECTION,original),before)
            c.close()
