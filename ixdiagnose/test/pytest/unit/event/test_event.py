import pytest

from ixdiagnose.event import event_callbacks
from ixdiagnose.exceptions import CallError


def correct_callback(progress, test):
    pass


def incorrect_callback(progress):
    pass


def test_clear_callbacks():
    event_callbacks.register(correct_callback)
    assert event_callbacks.CALLBACKS == [correct_callback]
    event_callbacks.clear()
    assert event_callbacks.CALLBACKS == []


@pytest.mark.parametrize('callback,should_work', [
    (
        correct_callback,
        True,
    ),
    (
        incorrect_callback,
        False,
    ),
    (
        'not a callable',
        False,
    )
])
def test_event_callbacks(callback, should_work):
    if should_work:
        assert event_callbacks.register(callback) is None
    else:
        with pytest.raises(CallError):
            event_callbacks.register(callback)
