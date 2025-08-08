import numpy as np
from PIL import Image

def floyd_steinberg_dithering(image):
    grayscale = image.convert("L")
    data = np.array(grayscale, dtype=np.float32)
    height, width = data.shape

    for y in range(height):
        for x in range(width):
            old_pixel = data[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            data[y, x] = new_pixel
            error = old_pixel - new_pixel

            if x + 1 < width:
                data[y, x + 1] += error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    data[y + 1, x - 1] += error * 3 / 16
                data[y + 1, x] += error * 5 / 16
                if x + 1 < width:
                    data[y + 1, x + 1] += error * 1 / 16

    return Image.fromarray(data.astype(np.uint8))

def generate_shares(binary_image):
    binary_data = np.array(binary_image, dtype=np.uint8) // 255
    height, width = binary_data.shape

    share1 = np.random.randint(0, 2, size=(height, width))
    share2 = np.random.randint(0, 2, size=(height, width))
    share3 = (binary_data ^ share1 ^ share2) % 2

    share1 *= 255
    share2 *= 255
    share3 *= 255

    return (
        Image.fromarray(share1.astype(np.uint8)),
        Image.fromarray(share2.astype(np.uint8)),
        Image.fromarray(share3.astype(np.uint8)),
    )

def reconstruct_image(share1, share2, share3):
    share1_data = np.array(share1, dtype=np.uint8) // 255
    share2_data = np.array(share2, dtype=np.uint8) // 255
    share3_data = np.array(share3, dtype=np.uint8) // 255

    reconstructed = (share1_data ^ share2_data ^ share3_data) * 255
    return Image.fromarray(reconstructed.astype(np.uint8))

# Main workflow
def main():
    input_image_path = "input.png"  # Replace with your image path
    input_image = Image.open(input_image_path)

    # Step 1: Convert to binary using Floyd-Steinberg dithering
    binary_image = floyd_steinberg_dithering(input_image)
    binary_image.save("binary_image.png")

    # Step 2: Generate shares
    share1, share2, share3 = generate_shares(binary_image)
    share1.save("share1_temp2.png")
    share2.save("share2_temp2.png")
    share3.save("share3_temp2.png")

    # Step 3: Reconstruct image
    reconstructed_image = reconstruct_image(share1, share2, share3)
    reconstructed_image.save("output_temp2.png")

if __name__ == "__main__":
    main()
