from rpi_spotify_shared.message_handler.spotify_artwork_messages import *


def test_encode_jpeg_as_message_and_decode_preserves_filename_and_data():
    filename = "wibble wobble"
    filedata = '🎶🎈🧨👍🦐🦑🦞🦆'.encode(encoding = 'UTF-8')

    message = convert_file_data_to_message_body(filename, filedata)

    decoded_name, decoded_data = convert_message_body_to_file_data(message)

    assert filename == decoded_name
    assert filedata == decoded_data

def test_encode_progress_as_message_preserves_values():
    so_far = 1234
    total = 45678

    message = convert_progress_to_message_body(so_far, total)

    decoded_so_far, decoded_total = convert_message_body_to_progress(message)

    assert so_far == decoded_so_far
    assert total == decoded_total