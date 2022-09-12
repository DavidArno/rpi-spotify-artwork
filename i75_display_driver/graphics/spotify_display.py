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
import hub75

class SpotifyDisplay:
    def __init__(this, hub75_matrix):
        this._hub = hub75_matrix
        this._black = hub75.color(0, 0, 0)
        this._dark_grey = hub75.color(64, 64, 64)
        this._mid_grey = hub75.color(128, 128, 128)
        this._light_grey = hub75.color(192, 192, 192)
        this.clear()

    def clear(this):
        this._foreground_layer = []
        this._background_layer = []

        for _ in range(64):
            this._foreground_layer.append(this._black_row())
            this._background_layer.append(this._black_row())

    def _black_row(this):
        row = []
        for _ in range(64):
            row.append(this._black)
        return row

    def _draw_indented_rectangle(this, x, y, width, height):
        this._draw_horizontal_line(this, x, y, width-1, this._dark_grey)
        this._draw_vertical_line(this, x, y+1, height-2, this._dark_grey)
        this._draw_horizontal_line(this, x+1, y + height - 1, width-1, this._light_grey)
        this._draw_vertical_line(this, x + width - 1, y+1, height-2, this._light_grey)
        this.set_pixel_colour(x + width - 1, y, this._mid_grey)
        this.set_pixel_colour(x, y + height - 1, this._mid_grey)
        this._flood_fill(x+1, y+1, width-2, height-2)

    def _draw_horizontal_line(this, x, y, width, colour):
        for offset in range(width):
            this.set_pixel_colour(x + offset, y, colour)

    def _draw_vertical_line(this, x, y, height, colour):
        for offset in range(height):
            this.set_pixel_colour(x, y + offset, colour)

    def _flood_fill(this, x, y, width, height, colour):
        for offset in range(width):
            this._draw_vertical_line(x + offset, y, height, colour)

    def set_pixel_colour(this, x, y, colour):
        