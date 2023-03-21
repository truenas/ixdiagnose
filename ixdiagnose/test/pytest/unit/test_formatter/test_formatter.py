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
])
def test_remove_keys(keys, input_data, expected_output):
    callback = remove_keys(keys)
    assert callback(input_data) == expected_output
