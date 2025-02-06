from dataclasses import dataclass
from typing import Callable
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


@dataclass
class ReceiverConfiguration:
    host: str
    port: int
    buffer_size: int
    data_receiver: Callable[[bytes], None]


@dataclass
class SenderConfiguration:
    host: str
    port: int
    buffer_size: int
    data_provider: Callable[[], bytes | None]
    time_between_calls: float


class _ReceiverSocket:
    def __init__(self, socket: socket, configuration: ReceiverConfiguration):
        self._socket = socket
        self._configuration = configuration

    def fileno(self) -> int:
        return self._socket.fileno()

    def fetch_data_from_socket_and_pass_to_receiver(self) -> None:
        data = self._socket.recv(self._configuration.buffer_size)
        self._configuration.data_receiver(data)


class _SenderSocket:
    def __init__(self, socket: socket, configuration: SenderConfiguration):
        self._socket = socket
        self._configuration = configuration

    def fileno(self) -> int:
        return self._socket.fileno()

    def fetch_data_from_sender_and_pass_to_socket(self):
        data = self._configuration.data_provider()

        if data is not None:
            self._socket.send(data)
            
class SocketHandler:

    def __init__(
            self, *,
            select_timeout: float | None = None,
            receivers: list[ReceiverConfiguration] = [],
            senders: list[SenderConfiguration] = []) -> None:
        self._select_timeout = select_timeout
        self._receiver_sockets = self._configure_receivers(receivers)
        self._senders_sockets = self._configure_senders(senders)

    def _configure_receivers(self, receivers: list[ReceiverConfiguration]) -> list[_ReceiverSocket]:
        receiver_sockets: list[_ReceiverSocket] = []

        for receiver in receivers:
            sock = socket(family=AF_INET, type=SOCK_STREAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((receiver.host, receiver.port))
            sock.listen(1)

            receiver_sockets.append(_ReceiverSocket(sock, receiver))

        return receiver_sockets

    def _configure_senders(self, senders: list[SenderConfiguration]) -> list[_SenderSocket]:
        sender_sockets: list[_SenderSocket] = []

        for sender in senders:
            sock = socket(samily=AF_INET, type=SOCK_STREAM)
            sock.connect((sender.host, sender.port))

            sender_sockets.append(_SenderSocket(sock, sender))

        return sender_sockets