SAMPLE_POST = {
    'tags': ['[Sample]'],
    'description': 'sample post api',
    'parameters': [
        {
            'name': 'id',
            'description': 'uuid',
            'in': 'json',
            'type': 'str',
            'required': False
        }
    ],
    'responses': {
        '200': {
            'description': '지원자 검색 성공',
        }
    }
}
