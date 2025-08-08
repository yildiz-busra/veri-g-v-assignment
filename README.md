# Visual Cryptography Assignment

This repository implements visual cryptography techniques in Python, enabling secure image sharing and reconstruction. Visual cryptography is a cryptographic technique that encodes visual information (such as images) into multiple shares; these shares individually reveal no information about the original, but when overlaid, reconstruct the secret image.

## Features

- **Floyd-Steinberg Dithering**: Converts grayscale images to binary (black-and-white) images using error diffusion for improved visual quality.
- **Share Generation (2-out-of-2 & 3-out-of-3)**:
  - `2-out-of-2.py` creates two shares for a binary image.
  - `main.py` supports generating three shares and reconstructing the image with all shares.
- **Image Reconstruction**: Overlays shares to reveal the original image.
- **Python & PIL-based Implementation**: Uses numpy and Pillow for image processing.

## Usage

### Requirements

- Python 3.x
- Pillow (`pip install pillow`)
- Numpy (`pip install numpy`)

### Example Workflow

#### 2-out-of-2 Scheme

1. **Dither Original Image**  
   Converts `input.png` to a binary image:
   ```python
   binaryImg = dither("input.png")
   ```
   Output: `output-floyd-steinberg.png`

2. **Generate Shares**  
   Generates two visual cryptography shares:
   ```python
   generateShares(binaryImg)
   ```
   Output: `share1.png`, `share2.png`

3. **Overlay Shares**  
   Overlays the shares to reconstruct the secret image:
   ```python
   overlay_shares("share1.png", "share2.png", "output.png")
   ```

#### 3-out-of-3 Scheme

In `main.py`:

1. Place your input image as `input.png`.
2. Run the script to generate a binary image and three shares:
   ```
   python main.py
   ```
   Output:
   - `binary_image.png`
   - `share1_temp2.png`
   - `share2_temp2.png`
   - `share3_temp2.png`
   - `output_temp2.png` (reconstructed image)

## How It Works

- **Dithering**: Converts images to black-and-white using Floyd-Steinberg error diffusion.
- **Share Generation**: Randomizes pixel patterns so each share reveals no information alone.
- **Overlaying**: Combines shares using pixel-wise logical operations to reconstruct the original.

## Author

[Busra Yildiz](https://github.com/yildiz-busra)

---

*For educational and research purposes. Contributions and feedback are welcome!*
