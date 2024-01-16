from dataclasses import dataclass
from typing import Callable
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


@dataclass
class _ReceiverConfiguration:
    host: str
    port: int
    buffer_size: int
    data_receiver: Callable[[bytes], None]


@dataclass
class _SenderConfiguration:
    host: str
    port: int
    buffer_size: int
    data_provider: Callable[[], bytes | None]
    time_between_calls: float


class _ReceiverSocket:
    def __init__(self, socket: socket, configuration: _ReceiverConfiguration):
        self._socket = socket
        self._configuration = configuration

    def fileno(self) -> int:
        return self._socket.fileno()

    def send_data_to_receiver(self) -> None:
        data = self._socket.recv(self._configuration.buffer_size)
        self._configuration.data_receiver(data)


class SocketHandler:

    def __init__(
            self, *,
            select_timeout: float | None = None,
            receivers: list[_ReceiverConfiguration] = [],
            senders: list[_SenderConfiguration] = []) -> None:
        self._select_timeout = select_timeout
        self._receiver_sockets = self._configure_receivers(receivers)
        self.senders = senders

    def _configure_receivers(self, receivers: list[_ReceiverConfiguration]) -> list[_ReceiverSocket]:
        receiver_sockets: list[_ReceiverSocket] = []

        for receiver in receivers:
            sock = socket(family=AF_INET, type=SOCK_STREAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((receiver.host, receiver.port))
            sock.listen(1)

            receiver_sockets.append(_ReceiverSocket(sock, receiver))

        return receiver_sockets
