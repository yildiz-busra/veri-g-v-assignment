import numpy as np
import random
from PIL import Image

def dither(path):
    img = Image.open(path).convert('L')
    image = np.array(img)
    threshold = 128
    binaryImg = np.zeros_like(image, dtype=np.uint8)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            oldPixel = image[y, x]
            newPixel = 255 if oldPixel > threshold else 0
            binaryImg[y, x] = newPixel
            error = oldPixel - newPixel
            if x + 1 < image.shape[1]:
                image[y, x + 1] += error * 7 / 16
            if y + 1 < image.shape[0]:
                if x > 0:
                    image[y + 1, x - 1] += error * 3 / 16
                image[y + 1, x] += error * 5 / 16
                if x + 1 < image.shape[1]:
                    image[y + 1, x + 1] += error * 1 / 16
    return binaryImg

def generate_pattern(pixel):

    if pixel == 0:  # siyah pixel
        return random.choice([
            ([1, 0], [0, 1], [1, 0]),
            ([0, 1], [1, 0], [0, 1])
        ])
    else:  # beyazpixel
        return random.choice([
            ([1, 0], [1, 0], [1, 0]),
            ([0, 1], [0, 1], [0, 1])
        ])
    
def generateShares(image, output_paths):

    if len(output_paths) != 3:
        raise ValueError("You must provide exactly 3 output paths for the shares.")

    image_array = np.array(image)
    height, width = image_array.shape

    share1 = np.zeros((height, width * 2), dtype=np.uint8)
    share2 = np.zeros((height, width * 2), dtype=np.uint8)
    share3 = np.zeros((height, width * 2), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pattern = generate_pattern(image_array[i, j])

            share1[i, j * 2:j * 2 + 2] = pattern[0]
            share2[i, j * 2:j * 2 + 2] = pattern[1]
            share3[i, j * 2:j * 2 + 2] = pattern[2]


    Image.fromarray(share1 * 255).save(output_paths[0])
    Image.fromarray(share2 * 255).save(output_paths[1])
    Image.fromarray(share3 * 255).save(output_paths[2])

    print("Shares have been saved.")
    
# def saveShares(shares, outputPaths):
#     for share, path in zip(shares, outputPaths):
#         shareImg = Image.fromarray(share)
#         shareImg.save(path)

def overlay_shares(share1, share2, share3, output):
    share1 = Image.open(share1)
    share2 = Image.open(share2)
    share3 = Image.open(share3)
    assert share1.size == share2.size == share3.size, "Shares must be the same size."
    result = Image.new('1', share1.size)

    pixelShare1 = share1.load()
    pixelShare2 = share2.load()
    pixelShare3 = share3.load()
    pixels_result = result.load()

    width, height = share1.size
    for x in range(width):
        for y in range(height):
            pixels_result[x, y] = pixelShare1[x, y] & pixelShare2[x, y] & pixelShare3[x, y]

    result.save(output)
    print(f"Overlayed image saved as '{output}'.")

def main():
    inputPath = "input2.png"
    outputPaths = ["share1-main2.png", "share2-main2.png", "share3-main2.png"]

    binaryImg = dither(inputPath)
    generateShares(binaryImg, outputPaths)
    overlay_shares("share1-main2.png", "share2-main2.png", "share3-main2.png", "output-main2.png")
    #saveShares(shares, outputPaths)

    

