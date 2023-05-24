from PIL import Image
import numpy as np


def conv2tuple(lists_in_list: np.ndarray):
    box = []
    for list in lists_in_list:
        box.append(tuple(list))
    return box


img = Image.open('celluloid-shot0001.jpg', 'r')
width, height = img.size

# img.show()

pixels = np.array(img.getdata())

print(width * (height - 1))
pixels_copy = pixels.copy()
factor = 2
scalar = factor / 255

i = 0
for pixel in pixels:
    pixel[0] = round(pixel[0] * scalar) * (255 / factor)
    pixel[1] = round(pixel[1] * scalar) * (255 / factor)
    pixel[2] = round(pixel[2] * scalar) * (255 / factor)

    err_R = pixels_copy[i, 0] - pixel[0]
    err_G = pixels_copy[i, 1] - pixel[1]
    err_B = pixels_copy[i, 2] - pixel[2]

    # if i == 0 or i % width == 0 or i % (width - 1) == 0 or i >= width * (height - 1):
    #     continue
    # else:
    try:
        pixels[i + 1, 0] += int(7 / 16 * err_R)
        pixels[i + 1, 1] += int(7 / 16 * err_G)
        pixels[i + 1, 2] += int(7 / 16 * err_B)
    except IndexError:
        continue
    try:
        pixels[i + width, 0] += int(5 / 16 * err_R)
        pixels[i + width, 0] += int(5 / 16 * err_G)
        pixels[i + width, 0] += int(5 / 16 * err_B)
    except IndexError:
        continue
    try:
        pixels[i + width + 1, 0] += int(3 / 16 * err_R)
        pixels[i + width + 1, 1] += int(3 / 16 * err_G)
        pixels[i + width + 1, 2] += int(3 / 16 * err_B)
    except IndexError:
        continue
    try:
        pixels[i + width - 1, 0] += int(1 / 16 * err_R)
        pixels[i + width - 1, 1] += int(1 / 16 * err_G)
        pixels[i + width - 1, 2] += int(1 / 16 * err_B)
    except IndexError:
        continue
    i += 1


img.putdata(conv2tuple(pixels))
img = img.convert("L")
img.show('quantised')