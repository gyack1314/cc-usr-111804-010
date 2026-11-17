"""将已接收原文和来源化实体写入同一事务。"""
import hashlib
import json
import sqlite3
from .domain import decode

SCHEMA="""
CREATE TABLE IF NOT EXISTS receipts(
  collection TEXT NOT NULL, body_sha256 TEXT NOT NULL, source_url TEXT NOT NULL,
  status INTEGER NOT NULL, raw BLOB NOT NULL,
  PRIMARY KEY(collection,body_sha256));
CREATE TABLE IF NOT EXISTS entities(
  collection TEXT NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL,
  version TEXT NOT NULL, receipt_sha256 TEXT NOT NULL, payload_json TEXT NOT NULL,
  PRIMARY KEY(collection,entity_type,entity_id,version),
  FOREIGN KEY(collection,receipt_sha256) REFERENCES receipts(collection,body_sha256));
"""

def connect(path):
    c=sqlite3.connect(path)
    c.execute('PRAGMA foreign_keys=ON')
    c.executescript(SCHEMA)
    return c

def receive(c, collection, raw, receipt):
    if receipt['status']!=200:raise ValueError('来源响应非成功正文')
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=receipt['body_sha256']:raise ValueError('响应收据与原文不一致')
    rows=decode(raw,receipt)
    with c:
        c.execute('INSERT OR IGNORE INTO receipts VALUES(?,?,?,?,?)',
                  (collection,digest,receipt['url'],receipt['status'],raw))
        for row in rows:
            payload=json.dumps(row['payload'],ensure_ascii=False,sort_keys=True)
            key=(collection,row['type'],row['id'],row['version'])
            prior=c.execute('SELECT receipt_sha256,payload_json FROM entities WHERE collection=? AND entity_type=? AND entity_id=? AND version=?',key).fetchone()
            if prior and prior!=(digest,payload):raise ValueError('同一实体版本的原文发生冲突')
            c.execute('INSERT OR IGNORE INTO entities VALUES(?,?,?,?,?,?)',(*key,digest,payload))
    return digest

def entities(c,collection):
    return [dict(type=row[0],id=row[1],version=row[2],source=row[3],payload=json.loads(row[4]))
            for row in c.execute('SELECT entity_type,entity_id,version,receipt_sha256,payload_json FROM entities WHERE collection=? ORDER BY entity_type,entity_id,version',(collection,))]
