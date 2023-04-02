BASE_REPORT_SCHEMA = {
    'type': 'object',
    'properties': {
        'execution_time': {'type': 'number'},
        'execution_error': {'type': ['string', 'null']},
        'execution_traceback': {'type': ['string', 'null']},
    }
}
