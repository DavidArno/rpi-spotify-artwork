
from typing import Callable, NewType

MessageHeader = NewType('MessageHeader', str)
MessageBody = NewType('MessageBody', str)

MessageHandler = Callable[[MessageBody], bool]

MessageBrokers = NewType('MessageBrokers', dict[MessageHeader, MessageHandler])