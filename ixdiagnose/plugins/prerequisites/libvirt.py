import os

from .base import Prerequisite


CONTAINERS_LIBVIRT_SOCKET = '/run/truenas_libvirt/libvirt-sock'


class LibvirtContainersPrerequisite(Prerequisite):

    def __init__(self):
        super().__init__(True)
        self.cache_key = 'libvirt_containers_socket'

    def evaluate_impl(self) -> bool:
        return os.path.exists(CONTAINERS_LIBVIRT_SOCKET)

    def __str__(self):
        return 'libvirt containers socket existence check'
