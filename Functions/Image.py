from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()


class Image2Ascii:
    scale = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    def __init__(self, path):
        try:
            self._image = Image.open(path)
        except FileNotFoundError:
            print(f"There is no image in {path}")

    def resize_image(self, new_width=200):
        width, height = self._image.size
        factor = height / width
        new_height = int(factor * new_width)
        self._image = self._image.resize((new_width, new_height))

    def turn_to_gray(self):
        self._image = self._image.convert('L')

    def pixels_to_ascii(self):
        pixels = self._image.getdata()
        characters = "".join([self.scale[pixel * (len(self.scale) - 1) // 255] for pixel in pixels])
        return (characters)

    def convert(self, new_width):
        self.resize_image(new_width)
        self.turn_to_gray()
        new_image_str = self.pixels_to_ascii()
        pixel_count = len(new_image_str)
        ascii_image = '\n'.join(new_image_str[i:(i + new_width)] for i in range(0, pixel_count, new_width))
        with open('Test.txt', 'w') as f:
            f.write(ascii_image)

if __name__ == '__main__':
    file_path = f"{os.getenv('folder_path')}/TestImages/2.jpg"
    a = Image2Ascii(file_path)
    a.convert(1000)
