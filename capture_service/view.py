"""按本项目约定展示已接收资料与明确缺口。"""
from .ledger import entities
from .domain import assess
from .collection import coverage
from .primary_records import current as primary_records
from .supporting_records import current as supporting_records

def overview(c,collection):
    rows=entities(c,collection)
    result=assess(rows)
    result['collection']=collection
    result['records']=[{'type':r['type'],'id':r['id'],'version':r['version'],'source_sha256':r['source']} for r in rows]
    result['coverage']=coverage(c,collection)
    result['primary_records']=primary_records(c,collection)
    result['supporting_records']=supporting_records(c,collection)
    return result
