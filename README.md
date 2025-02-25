# Image Steganography Tool

This project is a Python-based tool for encoding and decoding secret messages within images using steganography. The tool supports various image formats and ensures secure message encryption using a password.

## Features

- Encode secret messages into images
- Decode hidden messages from images
- Supports multiple image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`
- Ensures secure message encryption using a password
- Handles images up to 5MB in size
- Provides clear user interface with step-by-step prompts

## Requirements

- Python 3.x
- Pillow library
- NumPy library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/steganography-tool.git
    cd steganography-tool
    ```

2. Install the required libraries:
    ```bash
    pip install pillow numpy
    ```

## Usage

Run the script using Python:
```bash
python stego.py
