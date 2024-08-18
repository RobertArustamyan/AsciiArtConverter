from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os

load_dotenv()


class Image2Ascii:
    scale = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    def __init__(self, path):
        try:
            self._image = Image.open(path)
            self.path = path
        except FileNotFoundError:
            print(f"There is no image in {path}")

    def resize_image(self, new_width: int = 200) -> None:
        """
        Changes picture size
        :param new_width: New width of picture
        :return: Modifies image with new width and height
        """
        width, height = self._image.size
        factor = height / width
        new_height = int(factor * new_width)
        self._image = self._image.resize((new_width, new_height))

    def turn_to_gray(self) -> None:
        """
        Converts picture to gray
        :return: None
        """
        self._image = self._image.convert('L')

    def pixels_to_ascii(self) -> str:
        """
        Makes a character tuple depending on pixel
        :return: Tuple of characters
        """
        pixels = self._image.getdata()
        characters = "".join([self.scale[pixel * (len(self.scale) - 1) // 255] for pixel in pixels])
        return characters

    def convert_to_string(self, new_width: int = 200) -> str:
        """
        Converts image to ascii string. Is used if -s or --string
        :param new_width: New width of picture
        :return: Returns string that is representation of picture in ascii
        """
        self.resize_image(new_width)
        self.turn_to_gray()
        new_image_str = self.pixels_to_ascii()
        pixel_count = len(new_image_str)
        ascii_string = '\n'.join(new_image_str[i:(i + new_width)] for i in range(0, pixel_count, new_width))
        return ascii_string

    def ascii_to_image(self, ascii_string: str, font_size: int = 16, background: tuple = (40, 44, 52),
                       text_color: tuple = (182, 183, 183),for_video:bool = False) -> None:
        """
        :param ascii_string: String representation of picture
        :param font_size: Size of each character
        :param background: Background color in RGB format
        :param text_color: Text color in RGB format
        :param for_video: If true doesn't save image as a file
        :return: Saves an image in -ascii.png
        """
        lines = ascii_string.split('\n')
        height = len(lines)
        width = len(lines[0])

        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", font_size)

        image = Image.new('RGB', (width * (font_size - 6), height * font_size), color=background)
        draw = ImageDraw.Draw(image)

        for y, line in enumerate(lines):
            draw.text((5, y * font_size), line, font=font, fill=text_color)

        file_name = self.path.split('/')[-1].split('.')[0]
        if not for_video:
            image.save(f'{"/".join(self.path.split('/')[:-1])}/{file_name}-ascii.png')
        return image

    def convert(self, convert_to_image: bool, new_width: int = 200,for_video:bool = False):
        """
        Image to image and image to string convertation
        :param convert_to_image: If True converts to image else in string
        :param for_video: If true doesn't save image as a file
        :param new_width: Width of new image
        """
        if convert_to_image:
            ascii_str = self.convert_to_string(new_width)
            return self.ascii_to_image(ascii_str,for_video=for_video)
        else:
            ascii_str = self.convert_to_string(new_width)
            file_name = self.path.split('/')[-1].split('.')[0]
            with open(f"{"/".join(self.path.split('/')[:-1])}/{file_name}.txt", 'w') as f:
                f.write(ascii_str)

    def convert2color(self, new_width: int = 200, font_size: int = 16, background: tuple = (40, 44, 52),
                      colorness: bool = True):
        originalImage = Image.open(self.path).convert('RGB')

        width, height = originalImage.size
        factor = height / width
        new_height = int(factor * new_width)
        originalImage = originalImage.resize((new_width, new_height))

        pixels = originalImage.getdata()
        grayscaleImage = originalImage.convert('L')
        grayPixels = grayscaleImage.getdata()

        characters = "".join([self.scale[pixel * (len(self.scale) - 1) // 255] for pixel in grayPixels])
        pixelCount = len(characters)

        asciiString = '\n'.join(characters[i:(i + new_width)] for i in range(0, pixelCount, new_width))

        lines = asciiString.split('\n')
        height = len(lines)
        width = len(lines[0])

        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", font_size)
        image = Image.new('RGB', (width * (font_size - 6), height * font_size), color=background)
        draw = ImageDraw.Draw(image)

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if colorness:
                    color = pixels[y * new_width + x]
                else:
                    color = (182, 183, 183)

                draw.text((x * (font_size - 6), y * font_size), char, font=font, fill=color)

        file_name = self.path.split('/')[-1].split('.')[0]
        image.save(f'{"/".join(self.path.split('/')[:-1])}/{file_name}-ascii.png')
        return image

if __name__ == '__main__':
    file_path = f"{os.getenv('folder_path')}/TestImages/1.png"
    a = Image2Ascii(file_path)
    a.convert2color()