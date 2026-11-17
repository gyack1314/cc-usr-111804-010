"""解析来源身份及本项目公开资料字段。"""
import json
from pathlib import Path
CONTRACT=json.loads((Path(__file__).resolve().parents[1]/'docs'/'source-contract.json').read_text(encoding='utf-8'))
def decode(raw,receipt):
    doc=json.loads(raw.decode('utf-8'))
    if not all(k in doc for k in ('kind','id','revision')): raise ValueError('资料身份缺失')
    kind=doc['kind']
    if kind not in CONTRACT['roles']: raise ValueError('未知来源类型')
    if any(k not in doc for k in CONTRACT['required_fields'][kind]): raise ValueError('来源业务字段缺失')
    return [{'type':kind,'id':doc['id'],'version':doc['revision'],'payload':{k:v for k,v in doc.items() if k not in ('kind','id','revision')}}]
def assess(rows):
    return {'publishable':False,'reasons':['来源资料已接收，关联和完整范围尚待核对'],'received_types':sorted({r['type'] for r in rows}),'received_versions':len(rows),'candidate_relations':sorted({str(r['payload'].get(CONTRACT['relation_field'])) for r in rows})}
