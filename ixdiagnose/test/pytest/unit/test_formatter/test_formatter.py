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
    )
])
def test_remove_keys(keys, input_data, expected_output):
    callback = remove_keys(keys)
    assert callback(input_data) == expected_output
