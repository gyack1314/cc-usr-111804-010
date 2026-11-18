"""Receive a frozen source set with durable per-source progress."""
import json
from pathlib import Path
from .transport import Replay
from .ledger import receive

def initialize(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS collection_progress (
      collection TEXT NOT NULL, source_url TEXT NOT NULL,
      body_sha256 TEXT NOT NULL, received_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(collection, source_url, body_sha256))""")
    connection.commit()

def collect(connection, collection, manifest_path):
    """Replay every listed source, accepting already received bytes on restart."""
    initialize(connection)
    replay = Replay(manifest_path)
    result = []
    for step in replay.steps:
        request = step['request']
        raw, receipt = replay.request(request['method'], request['url'])
        digest = receive(connection, collection, raw, receipt)
        with connection:
            connection.execute(
                'INSERT OR IGNORE INTO collection_progress(collection,source_url,body_sha256) VALUES(?,?,?)',
                (collection, receipt['url'], digest))
        result.append(dict(source_url=receipt['url'], body_sha256=digest))
    return result

def progress(connection, collection):
    initialize(connection)
    return [dict(source_url=row[0], body_sha256=row[1], received_at=row[2])
            for row in connection.execute(
                'SELECT source_url,body_sha256,received_at FROM collection_progress WHERE collection=? ORDER BY source_url',
                (collection,))]
