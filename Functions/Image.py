from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os
import argparse

load_dotenv()


class Image2Ascii:
    scale = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def __init__(self, path):
        try:
            self._image = Image.open(path)
            self.path = path
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

    def convert_to_string(self, new_width=200):
        self.resize_image(new_width)
        self.turn_to_gray()
        new_image_str = self.pixels_to_ascii()
        pixel_count = len(new_image_str)
        ascii_string = '\n'.join(new_image_str[i:(i + new_width)] for i in range(0, pixel_count, new_width))
        return ascii_string

    def ascii_to_image(self, ascii_string, font_size=16,background=(40,44,52), text_color=(182,183,183)):
        lines = ascii_string.split('\n')
        height = len(lines)
        width = len(lines[0])
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", font_size)
        image = Image.new('RGB', ((width) * font_size, height * font_size), color=background)
        draw = ImageDraw.Draw(image)
        for y, line in enumerate(lines):
            draw.text((5, y * font_size), line, font=font,fill=text_color)

        file_name = self.path.split('/')[-1].split('.')[0]
        image.save(f'{"/".join(self.path.split('/')[:-1])}/{file_name}-ascii.png')

    def convert(self, convert_to_image:bool, new_width=200):
        if convert_to_image:
            ascii_str = self.convert_to_string(new_width)
            self.ascii_to_image(ascii_str)
        else:
            ascii_str = self.convert_to_string(new_width)
            file_name = self.path.split('/')[-1].split('.')[0]
            with open(f"{"/".join(self.path.split('/')[:-1])}/{file_name}.txt", 'w') as f:
                f.write(ascii_str)

if __name__ == '__main__':
    file_path = f"{os.getenv('folder_path')}/TestImages/1.png"
    a = Image2Ascii(file_path)
    a.ascii_to_image(a.convert_to_string(200))
