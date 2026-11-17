"""按本项目约定展示已接收资料与明确缺口。"""
from .ledger import entities
from .domain import assess

def overview(c,collection):
    rows=entities(c,collection)
    result=assess(rows)
    result['collection']=collection
    result['records']=[{'type':r['type'],'id':r['id'],'version':r['version'],'source_sha256':r['source']} for r in rows]
    return result
