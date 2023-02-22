from .base import Plugin
from .metrics import DirectoryTreeMetric, FileMetric


class SSL(Plugin):
    name = 'ssl'
    metrics = [
        DirectoryTreeMetric('certs', '/etc/certificates'),
        DirectoryTreeMetric('ssl_directory', '/etc/ssl'),
        FileMetric('openssl_config', '/etc/ssl/openssl.cnf'),
    ]
