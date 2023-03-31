from .artifact import gather_artifacts
from .event import event_callbacks, send_event
from .plugin import generate_plugins_debug


def generate_debug() -> None:
    send_event(0, 'Generating debug')
    generate_plugins_debug(total_percentage=90)
    gather_artifacts(90, total_percentage=10)
    send_event(100, 'Completed generating debug')
    event_callbacks.clear()
