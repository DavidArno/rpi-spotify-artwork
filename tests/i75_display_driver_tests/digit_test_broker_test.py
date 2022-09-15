from rpi_spotify_shared.message_handler import message_format
from i75_display_driver.brokers import digit_test_broker
from third_party import JPEGdecoder

def test_x():
    y = message_format.FAILURE
    x = digit_test_broker.DigitTestBroker(None)
    z = JPEGdecoder.jpeg()
    assert True