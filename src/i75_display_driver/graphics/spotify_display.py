################################################################################
# The display is made up of two layers:
# Background. This displays the track artwork and the container rectangle for
# the progress bar.
#
# Foreground. The progress bar and pause icon - when paused - are rendered in
# this layer.
#
# The overall image is then achieved by checking the foreground. If a pixel is
# black, then the background pixel is used. If not black, then the foreground 
# pixel is used instead.
################################################################################
# The functionality for rendering the track image sent by the controller 
# utilises the fact that the jpeg decoder (all spotify images are required to 
# be in jpeg format) calls
# callback(x, y, rgb) for each pixel. So the function 
# set_pixel_from_jpeg(x, y, rgb) is provided to be hooked directly into that
# functionality.
# This function automatically caters for the progress container. See below for 
# details
################################################################################
# The full set of functions provided are:
# __init(hub75_matrix) - provides the display handler with access to the lcd
# matrix.
#
# clear() - clears both layers to black. This can be called directly when 
# rendering a background image from cache as the cache data includes the
# progress container. 
# 
# initialise() - calls clear(), then renders the progress container into 
# the background layer. Call this before rendering a track image from jpeg data.
#
# set_pixel_from_jpeg(x, y, rgb) - as above. If the current background layer's
# pixel is black, it converts the rgb to a hub75 colour and stores that in the 
# pixel. If it's not black, it does nothing. This ensures that the progress
# container is left intact whilst drawing the image. This is why clear() must
# be called before rendering the image starts as otherwise all pixels - unless
# coincidently black - will be unchanged.
#
# set_pixel_colour(x, y, colour) - sets the background layer pixel at x,y to the
# specified hub75 colour. Used to set the background from a cached image. This
# will override all pixels including for the progress bar container.
#
# get_pixel_colour(x, y) - gets the hub75 colour of the specified background 
# layer pixel. Used to create cached images on "disk". Will provide progress bar
# container pixels too so that the whole background can be recreated from 
#
# render() - draws the contents of the two layers to the lcd matrix.

# pause() - draws the pause icon into the foreground layer. When render() is 
# next called, the pause icon will be shown.

# resume() - erases the pause icon into the foreground layer. When render() is 
# next called, no pause icon will be displayed.

# progress(total_time, so_far_time) - Updates the progress bar with the total
# progress (so_far_time / total_time * bar width. When render() is next called, 
# the progress bar will show the current progress.
################################################################################
import colours

class SpotifyDisplay:
    def __init__(self, hub75_matrix):
        self._hub = hub75_matrix
        self.clear()

    def clear(self):
        self._foreground_layer = []
        self._background_layer = []

        for _ in range(64):
            self._foreground_layer.append(self._black_row())
            self._background_layer.append(self._black_row())

    def initialise(self):
        self.clear()
        self._draw_indented_rectangle(self._background_layer, 6, 54, 52, 5)

    def set_pixel_from_jpeg(self, x, y, rgb):
        if (self.get_pixel_colour(x, y) == colours.BLACK):
            self.set_pixel_colour(x, y, colours.rbg_colour_to_hub75_colour(rgb))

    def set_pixel_colour(self, x, y, colour):
        self._background_layer[x][y] = colour

    def get_pixel_colour(self, x, y):
        return self._background_layer[x][y]

    def progress(self, total_time, so_far_time):
        width = int(so_far_time / total_time * 50)
        if width > 0:
            self._flood_fill(self._foreground_layer, 7, 55, width, 3, colours.PROGRESS_ILLUMINATED)
        elif width < 50:
            self._flood_fill(self._foreground_layer, 8 + width, 55, 50 - width, 3, colours.BLACK)

    def pause(self):
        self._draw_indented_rectangle(self._foreground_layer, 22, 11, 7, 32)
        self._draw_indented_rectangle(self._foreground_layer, 35, 11, 7, 32)

    def resume(self):
        self._flood_fill(self._foreground_layer, 22, 11, 7, 32, colours.BLACK)
        self._flood_fill(self._foreground_layer, 35, 11, 7, 32, colours.BLACK)
        
    def render(self):
        for x in range(64):
            for y in range(64):
                if (colour := self._foreground_layer[x][y]) != self._black:
                    self._hub.set_color(x, y, colour)
                else:
                     self._hub.set_color(x, y, self._background_layer[x][y])
        

    def _black_row(self):
        row = []
        for _ in range(64):
            row.append(self._black)
        return row

    def _draw_indented_rectangle(self, layer, x, y, width, height):
        self._draw_horizontal_line(layer, x, y, width-1, colours.DARK_GREY)
        self._draw_vertical_line(layer, x, y+1, height-2, colours.DARK_GREY)
        self._draw_horizontal_line(layer, x+1, y + height - 1, width-1, colours.LIGHT_GREY)
        self._draw_vertical_line(layer, x + width - 1, y+1, height-2, colours.LIGHT_GREY)
        self._set_pixel_colour(layer, x + width - 1, y, colours.MID_GREY)
        self._set_pixel_colour(layer, x, y + height - 1, colours.MID_GREY)
        self._flood_fill(layer, x+1, y+1, width-2, height-2)

    def _draw_horizontal_line(self, layer, x, y, width, colour):
        for offset in range(width):
            self.set_pixel_colour(layer, x + offset, y, colour)

    def _draw_vertical_line(self, layer, x, y, height, colour):
        for offset in range(height):
            self.set_pixel_colour(layer, x, y + offset, colour)

    def _flood_fill(self, layer, x, y, width, height, colour):
        for offset in range(width):
            self._draw_vertical_line(layer, x + offset, y, height, colour)

    def _set_pixel_colour(self, layer, x, y, colour):
        layer[x][y] = colour