import compatibility

if compatibility.running_as_cpython:
    from typing import Callable, NewType

    MessageHeader = NewType('MessageHeader', str)
    MessageBody = NewType('MessageBody', str)

    MessageHandler = Callable[[MessageBody], bool]

    MessageBrokers = NewType('MessageBrokers', dict[MessageHeader, MessageHandler]) # type: ignore
else:
    MessageHeader = str # type: ignore
    MessageBody = str # type: ignore
    MessageHandler = callable # type: ignore
    MessageBrokers = lambda x: x # type: ignore