"""解析来源所声明的身份；跨来源业务关系由具体产品补充。"""
import json

def decode(raw, receipt):
    doc = json.loads(raw.decode('utf-8'))
    if not all(key in doc for key in ('kind', 'id', 'revision')):
        raise ValueError('资料身份缺失')
    return [{'type': doc['kind'], 'id': doc['id'], 'version': doc['revision'],
             'payload': {key: value for key, value in doc.items()
                         if key not in ('kind', 'id', 'revision')}}]

def assess(rows):
    return {'publishable': False, 'reasons': ['跨来源归属和完整性尚待核对'],
            'received_types': sorted({row['type'] for row in rows}),
            'received_versions': len(rows)}
