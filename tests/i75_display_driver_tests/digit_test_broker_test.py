from hub75_display.display import Display
from hub75 import Hub75 # type: ignore
from i75_display_driver.test_views.digit_test_broker import DigitTestBroker

def test_rendering_four_after_zero_correctly_clears_zero_and_draws_four():
    display = Display(64, 64, Hub75(64, 64, None))
    broker = DigitTestBroker(display)

    broker.handle_digit_test_message('0')
    broker.handle_digit_test_message('4')

    assert display._bottom_layer[1][1:8] == [0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000]
    assert display._bottom_layer[2][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[3][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[4][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[5][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[6][1:8] == [0x000000, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x000000]
    assert display._bottom_layer[7][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[8][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[9][1:8] == [0x000000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[10][1:8] == [0x00000, 0xFFFFFF, 0x400000, 0x400000, 0xFFFFFF, 0x400000, 0x000000]
    assert display._bottom_layer[11][1:8] == [0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000, 0x000000]
    