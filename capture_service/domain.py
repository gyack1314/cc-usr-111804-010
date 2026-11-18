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
    """按当前双来源契约核对候选关联；后续来源事件仍待业务解释。"""
    left=sorted((r for r in rows if r['type']==CONTRACT['roles'][0]),key=lambda r:r['version'])
    right=sorted((r for r in rows if r['type']==CONTRACT['roles'][1]),key=lambda r:r['version'])
    pairs=[]
    for first in left:
        for second in right:
            a,b=first['payload'],second['payload']
            if a['interface_revision']==b['interface_revision']:
                pairs.append({'left_id':first['id'],'left_version':first['version'],
                              'right_id':second['id'],'right_version':second['version'],
                              'left_source':first['source'],'right_source':second['source']})
    return {'publishable':bool(pairs),'reasons':[] if pairs else ['接口说明与组件测试版次一致'],
            'received_types':sorted({r['type'] for r in rows}),
            'received_versions':len(rows),'matched_pairs':pairs,
            'candidate_relations':sorted({str(r['payload'].get(CONTRACT['relation_field'])) for r in rows})}
