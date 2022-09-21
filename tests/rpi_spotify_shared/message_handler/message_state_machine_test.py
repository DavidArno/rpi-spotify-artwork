from rpi_spotify_shared.message_handler import message_format
from rpi_spotify_shared.message_handler import message_state_machine
from rpi_spotify_shared.message_handler.message_types import MessageBody, MessageBrokers, MessageHeader 


class _EndOfDataToSend(Exception):
    pass

class _ReaderWriterAndBrokers:
    def __init__(this, data_to_send):
        this._data_to_send = data_to_send
        this._index = 0
        this._replies = []
        this._broker1_messages = []
        this._broker2_messages = []

    def read(this):
        if this._index >= len(this._data_to_send):
            raise _EndOfDataToSend()
        else:
            char = this._data_to_send[this._index]
            this._index += 1
            return char

    def write(this, message):
        this._replies.append(message)

    def broker1(this, body:MessageBody) -> bool:
        this._broker1_messages.append(body)
        return True

    def broker2(this, body:MessageBody) -> bool:
        this._broker2_messages.append(body)
        return False

    @property
    def replies(this):
        return this._replies

    @property
    def broker1_messages(this):
        return this._broker1_messages

    @property
    def broker2_messages(this):
        return this._broker2_messages

_broker1_header = MessageHeader("B1")
_broker2_header = MessageHeader("B2")

def _set_up_reader_writer_and_brokers(data_to_send) -> tuple[_ReaderWriterAndBrokers, MessageBrokers]:
    reader_writer_and_brokers = _ReaderWriterAndBrokers(data_to_send)
    broker_collection:MessageBrokers = MessageBrokers(
        {
            _broker1_header: reader_writer_and_brokers.broker1,
            _broker2_header: reader_writer_and_brokers.broker2
        }
    )

    return (reader_writer_and_brokers, broker_collection)

def test_sending_valid_message_results_in_it_being_processed_correctly():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.SUCCESS and \
           len(mock_read_write.broker1_messages) == 1 and \
           mock_read_write.broker1_messages[0] == '12345'

def test_sending_valid_message_results_in_fail_response_if_appropriate():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{_broker2_header}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.FAILURE and \
           len(mock_read_write.broker2_messages) == 1 and \
           mock_read_write.broker2_messages[0] == '12345'

def test_sending_two_valid_messages_results_in_them_being_processed_correctly():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'67890{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 2 and \
           mock_read_write.replies[0] == message_format.SUCCESS and \
           mock_read_write.replies[1] == message_format.SUCCESS and \
           len(mock_read_write.broker1_messages) == 2 and \
           mock_read_write.broker1_messages[0] == '12345' and \
           mock_read_write.broker1_messages[1] == '67890'

def test_sending_message_without_start_results_in_unexpected_end_and_no_broker_called():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.UNEXPECTED_MESSAGE_END and \
           len(mock_read_write.broker1_messages) == 0 

def test_sending_message_without_header_results_in_missing_header_and_no_broker_called():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.MISSING_HEADER and \
           len(mock_read_write.broker1_messages) == 0 

def test_sending_unknown_header_results_in_unknown_header_and_no_broker_called():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}wibble{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.UNKNOWN_HEADER and \
           len(mock_read_write.broker1_messages) == 0 and \
           len(mock_read_write.broker1_messages) == 0

def test_sending_message_without_body_results_in_unexpected_end_and_no_broker_called():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 1 and \
           mock_read_write.replies[0] == message_format.UNEXPECTED_MESSAGE_END and \
           len(mock_read_write.broker1_messages) == 0 

def test_message_handler_recovers_from_invalid_message_to_correctly_process_more():
    (mock_read_write, brokers) = _set_up_reader_writer_and_brokers(
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_START}'
        f'12345{message_format.MESSAGE_BODY_END}'
        f'{message_format.MESSAGE_START}{_broker1_header}{message_format.MESSAGE_BODY_END}'
        f'{message_format.MESSAGE_START}{_broker2_header}{message_format.MESSAGE_BODY_START}'
        f'67890{message_format.MESSAGE_BODY_END}'
    )

    try:
        message_state_machine.handle_messages(mock_read_write.read, mock_read_write.write, brokers)
    except(_EndOfDataToSend):
        pass

    assert len(mock_read_write.replies) == 3 and \
           mock_read_write.replies[0] == message_format.SUCCESS and \
           mock_read_write.replies[1] == message_format.UNEXPECTED_MESSAGE_END and \
           mock_read_write.replies[2] == message_format.FAILURE and \
           len(mock_read_write.broker1_messages) == 1 and \
           mock_read_write.broker1_messages[0] == '12345' and \
           len(mock_read_write.broker2_messages) == 1 and \
           mock_read_write.broker2_messages[0] == '67890'
