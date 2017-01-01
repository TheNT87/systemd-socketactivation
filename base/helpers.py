import socket,http
from systemd import daemon,journal

def get_systemd_socket(bind=True):
    """Recive socket form helpers"""
    SYSTEMD_FIRST_SOCKET_FD = 3
    socket_type = http.server.HTTPServer.socket_type
    address_family = http.server.HTTPServer.address_family
    if bind:
        journal.send("bound to real socket")
        return map_fds()[SYSTEMD_FIRST_SOCKET_FD]
    return socket.fromfd(SYSTEMD_FIRST_SOCKET_FD, address_family, socket_type)

def map_fds():
    fds = {}
    for frozen_fd in frozenset(daemon.listen_fds()):
        journal.send("processing fd: {0}".format(frozen_fd))
        if daemon.is_socket(frozen_fd):
            sock_obj = socket.socket(fileno=frozen_fd)
            journal.send("created socket: name={0}".format(sock_obj.getsockname()))
            fds[frozen_fd] = sock_obj
    return fds
