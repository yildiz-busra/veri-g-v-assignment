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

def generateShares(binaryImg, k=3):
    h, w = binaryImg.shape
    shares = [np.zeros((h, w), dtype=np.uint8) for _ in range(k)]

    for y in range(h):
        for x in range(w):
            if binaryImg[y, x] == 255:  # beyaz pixel
                pattern = [255] * k
            else:  # siiyah pixel
                pattern = [0] * k
                pattern[random.randint(0, k - 1)] = 255
            random.shuffle(pattern)
            for i in range(k):
                shares[i][y, x] = pattern[i]

    return shares

def saveShares(shares, outputPaths):
    for share, path in zip(shares, outputPaths):
        shareImg = Image.fromarray(share)
        shareImg.save(path)

def main():
    inputPath = "input2.png"
    outputPaths = ["share1-main.png", "share2-main.png", "share3-main.png"]

    binaryImg = dither(inputPath)
    shares = generateShares(binaryImg, k=3)

    saveShares(shares, outputPaths)

    print("Shares have been saved.")

if __name__ == "__main__":
    main()