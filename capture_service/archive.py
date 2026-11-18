"""Preserve the sources behind a released collection view."""
import json
from .view import overview

def initialize(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS released_views (
      collection TEXT NOT NULL, revision INTEGER NOT NULL,
      released_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
      view_json TEXT NOT NULL,
      PRIMARY KEY(collection, revision))""")
    connection.commit()

def release(connection, collection):
    initialize(connection)
    current = overview(connection, collection)
    row = connection.execute(
        'SELECT COALESCE(MAX(revision), 0) FROM released_views WHERE collection=?',
        (collection,)).fetchone()
    revision = row[0] + 1
    with connection:
        connection.execute('INSERT INTO released_views(collection,revision,view_json) VALUES(?,?,?)',
                           (collection, revision, json.dumps(current, ensure_ascii=False, sort_keys=True)))
    return revision

def get(connection, collection, revision):
    initialize(connection)
    row = connection.execute('SELECT view_json FROM released_views WHERE collection=? AND revision=?',
                             (collection, revision)).fetchone()
    if row is None:
        raise KeyError((collection, revision))
    return json.loads(row[0])
