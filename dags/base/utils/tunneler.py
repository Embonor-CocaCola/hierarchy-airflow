from logging import info, warn

from airflow.providers.ssh.hooks.ssh import SSHHook

from config.expos_service.settings import ES_SSH_CONN_ID


class Tunneler():
    def __init__(self, remote_port, remote_host, local_port):
        self.hook = SSHHook(ssh_conn_id=ES_SSH_CONN_ID)
        self.tunnel = self.hook.get_tunnel(remote_port=remote_port, remote_host=remote_host, local_port=local_port)
        self.clients = 0

    def __enter__(self):
        self.clients += 1
        if self.clients == 1:
            self.open_tunnel()
        else:
            warn('Tunnel already opened')

    def __exit__(self, type, value, traceback):
        self.clients -= 1
        if self.clients == 0:
            self.close_tunnel()

    def open_tunnel(self):
        self.tunnel.start()
        info('Tunnel started')

    def close_tunnel(self):
        self.tunnel.close()
        info('Tunnel stopped')
