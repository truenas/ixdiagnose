import pytest

from ixdiagnose.utils.formatter import remove_keys


@pytest.mark.parametrize('keys,input_data,expected_output', [
    (
        ['bindpw'],
        {
            'id': 1,
            'domainname': '',
            'bindname': '',
            'bindpw': '',
        },
        {
            'id': 1,
            'domainname': '',
            'bindname': '',
        },
    ),
    (
        ['bindpw', 'bindname'],
        {
            'id': 1,
            'domainname': '',
            'bindname': '',
            'bindpw': '',
        },
        {
            'id': 1,
            'domainname': '',
        },
    ),
    (
        ['bindpw', 'bindname'],
        [
            {
                'id': 1,
                'domainname': 'domain1',
                'bindname': '',
                'bindpw': '',
            },
            {
                'id': 2,
                'domainname': 'domain2',
                'bindname': '',
                'bindpw': '',
            },
        ],
        [
            {
                'id': 1,
                'domainname': 'domain1',
            },
            {
                'id': 2,
                'domainname': 'domain2',
            },
        ],
    ),
    (
        ['attributes.password'],
        {
            'id': 1,
            'domainname': '',
            'bindname': '',
            'bindpw': '',
            'attributes': {
                'id': 1,
                'password': 123
            }
        },
        {
            'id': 1,
            'domainname': '',
            'bindname': '',
            'bindpw': '',
            'attributes': {
                'id': 1,
            }
        },
    ),
    (
        ['devices.attributes.password'],
        [
          {
            'id': 1,
            'name': '',
            'devices': [
              {
                'id': 1,
                'attributes': {
                  'port': 5910,
                  'password': '1',
                },
              }
            ],
          },
        ],
        [
          {
            'id': 1,
            'name': '',
            'devices': [
              {
                'id': 1,
                'attributes': {
                  'port': 5910,
                },
              }
            ],
          },
        ],
    ),
    (
            ['devices.attributes.credentials.password'],
            [
              {
                'id': 1,
                'name': '',
                'devices': [
                  {
                    'id': 1,
                    'attributes': {
                      'port': 5910,
                      'credentials': {
                          'name': 'test',
                          'password': 1234
                      },
                    },
                  }
                ],
              },
            ],
            [
              {
                'id': 1,
                'name': '',
                'devices': [
                  {
                    'id': 1,
                    'attributes': {
                      'port': 5910,
                        'credentials': {
                            'name': 'test'
                        }
                    },
                  }
                ],
              },
            ],
    ),
])
def test_remove_keys(keys, input_data, expected_output):
    callback = remove_keys(keys)
    assert callback(input_data) == expected_output
