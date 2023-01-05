from PIL import Image

def checker_board_colour(x: int, y: int):
    if x % 2 == 0:
        return 170 if y % 2 == 0 else 255
    else:
        return 0 if y % 2 == 0 else 85

image = Image.open("images/__experiments, ideas etc__/red-map.png")
rgb_image = image.convert('RGB')
count = 0

for x in range(image.width):
    for y in range(image.height):
        c = checker_board_colour(x, y)
        r, _, _ = rgb_image.getpixel((x, y))

        if r == 255:
            rgb_image.putpixel((x, y), (c, c, c))
            count += 1

rgb_image.save("images/__experiments, ideas etc__/check-map.png", "PNG")

print(count)