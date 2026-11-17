"""只读重放合成的来源交互并展示当前接收状态。"""
import argparse
import json
from .transport import Replay
from .ledger import connect,receive
from .view import overview

def main():
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=['inspect'])
    p.add_argument('manifest')
    args=p.parse_args()
    replay=Replay(args.manifest)
    db=connect(':memory:')
    collection='robot-010'
    for step in replay.steps:
        request=step['request']
        raw,receipt=replay.request(request['method'],request['url'])
        receive(db,collection,raw,receipt)
    print(json.dumps(overview(db,collection),ensure_ascii=False,indent=2))
    db.close()

if __name__=='__main__':main()
