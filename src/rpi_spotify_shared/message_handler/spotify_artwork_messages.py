import base64
from rpi_spotify_shared.message_handler.message_types import MessageBody

_NAME_AND_DATA_SEPARATOR = '-'
_ASCII = 'ascii'

def convert_file_data_to_message_body(filename:str, filedata:bytes) -> MessageBody:
    base64_filedata = base64.b64encode(filedata).decode(encoding = _ASCII)
    return MessageBody(filename + _NAME_AND_DATA_SEPARATOR + base64_filedata)

def convert_message_body_to_file_data(message_body:MessageBody) -> tuple[str, bytes]:
    (file_name, encoded_file_data) = message_body.split(_NAME_AND_DATA_SEPARATOR)
    file_data = base64.b64decode(encoded_file_data)
    return (file_name, file_data)

def convert_progress_to_message_body(so_far_time:int, total_time:int) -> MessageBody:
    return MessageBody(f"{so_far_time}{_NAME_AND_DATA_SEPARATOR}{total_time}")

def convert_message_body_to_progress(message_body:MessageBody) -> tuple[int, int]:
    so_far_time, total_time = [int(x) for x in message_body.split(_NAME_AND_DATA_SEPARATOR)]
    return so_far_time, total_time