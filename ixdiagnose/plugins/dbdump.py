from ixdiagnose.utils.command import Command

from .base import Plugin
from .metrics import CommandMetric


class DatabaseDump(Plugin):
    name = 'dbdump'
    metrics = [
        CommandMetric('dbdump', [
            Command(['/usr/local/bin/sqlite3fn', '/data/freenas-v1.db', '.dump'], 'Database Dump', serializeable=False),
        ]),
    ]
