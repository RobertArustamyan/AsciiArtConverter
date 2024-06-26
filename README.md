[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pillow Version](https://img.shields.io/badge/Pillow-8.3.2-green?style=for-the-badge&logo=pillow&logoColor=white)](https://python-pillow.org/)
[![MoviePy Version](https://img.shields.io/badge/MoviePy-1.0.3-ff69b4?style=for-the-badge&logo=moviepy&logoColor=white)](https://zulko.github.io/moviepy/)

# ASCII Art Converter

This project converts images and videos into ASCII art. It can transform a single image to an ASCII string representation (saved as an image) and convert video files into ASCII art videos.

## Features

- Convert an image to an ASCII art image.
- Convert a video to an ASCII art video.
- Supports various image and video formats.

## Demo
#### Video to Ascii Video
<p align="center">
  <img src="Demo/1.gif" alt="Demo Video" height="250" width="300">
  <img src="Demo/1-ascii.gif" alt="Demo ASCII Video" height="250" width="300">
</p>

#### Image to Ascii Image
<p align="center">
  <img src="Demo/1.png" alt="Demo Image" height="150" width="300">
  <img src="Demo/1-ascii.png" alt="Demo Ascii Image" height="150" width="300">
</p>

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RobertArustamyan/AsciiArtConverter.git
    ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create .env file and configurate the path to your project
   
## Usage
1. Image to Ascii
   ```bash
   python main.py path/to/input-image.png new_width -s/--string
   ```
2. Image to Image
   ```bash
   python main.py path/to/input-image.png new_width -i/--image
   ```
3. Video to Video

   ```bash
   python main.py path/to/video.mp4 new_width -v/--video
   ```
