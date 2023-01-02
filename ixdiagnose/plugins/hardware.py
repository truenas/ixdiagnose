from .base import Plugin, CmdMetric, Cmd


class ArchMetric(CmdMetric):
    cmds = [
       Cmd(command=["uname", "-m"]),
    ]


class Hardware(Plugin):
    name = 'hardware'
    metrics = [
        ArchMetric()
    ]
