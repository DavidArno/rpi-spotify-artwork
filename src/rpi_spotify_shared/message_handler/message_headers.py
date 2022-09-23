from rpi_spotify_shared.message_handler.message_types import MessageHeader

TEST_DIGIT = MessageHeader('test-d')

DISPLAY_ARTWORK = MessageHeader('spot-d')
SAVE_AND_DISPLAY_ARTWORK = MessageHeader('spot-s')
PAUSE = MessageHeader('spot-p')
RESUME = MessageHeader('spot-r')
UPDATE_PROGRESS = MessageHeader('spot-u')