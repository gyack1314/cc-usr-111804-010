"""核对来源、解释、账本与可见状态的一条完整业务链。"""
import unittest
from pathlib import Path
from capture_service.transport import Replay
from capture_service.ledger import connect,receive
from capture_service.view import overview

ROOT=Path(__file__).resolve().parents[1]
COLLECTION='robot-010'

class Integration(unittest.TestCase):
    def test_receipts_and_domain_state(self):
        replay=Replay(ROOT/'data'/'normal.json')
        db=connect(':memory:')
        for step in replay.steps:
            request=step['request']
            raw,receipt=replay.request(request['method'],request['url'])
            receive(db,COLLECTION,raw,receipt)
        view=overview(db,COLLECTION)
        self.assertGreaterEqual(len(view['records']),2)
        self.assertFalse(view['publishable'])
        self.assertTrue(view['reasons'])
        self.assertEqual(db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0],len(replay.steps))
        db.close()

    def test_authorization_scope(self):
        replay=Replay(ROOT/'data'/'normal.json')
        request=replay.steps[0]['request']
        with self.assertRaises(ValueError):
            replay.request(request['method'],request['url'],credential_scope='https://elsewhere.example.test')
        self.assertEqual(replay.position,0)

    def test_same_version_conflict_rolls_back(self):
        replay=Replay(ROOT/'data'/'conflict.json')
        db=connect(':memory:')
        first=replay.steps[0]['request']
        raw,receipt=replay.request(first['method'],first['url'])
        receive(db,COLLECTION,raw,receipt)
        before=overview(db,COLLECTION)
        next_request=replay.steps[1]['request']
        other,other_receipt=replay.request(next_request['method'],next_request['url'])
        with self.assertRaises(ValueError):receive(db,COLLECTION,other,other_receipt)
        self.assertEqual(overview(db,COLLECTION),before)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0],1)
        db.close()
