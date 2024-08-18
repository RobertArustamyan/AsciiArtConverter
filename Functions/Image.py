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

    def imageToAsciiString(self) -> str:
        """
        Converts image to ascii string.
        :return: ascii string.
        """
        pixels = self._image.getdata()
        characters = "".join([self.scale[pixel * (len(self.scale) - 1) // 255] for pixel in pixels])
        return characters

    def convertToString(self, new_width: int = 200) -> str:
        """
        Adds '\n' to converted ascii string and makes it right sizes(width,height).
        :param new_width: Width of image.
        :return: Ascii string in correct sizes.
        """
        self._image = self.resizeImage(self._image, new_width)
        self._image.convert('L')
        new_image_str = self.imageToAsciiString()
        pixel_count = len(new_image_str)
        ascii_string = '\n'.join(new_image_str[i:(i + new_width)] for i in range(0, pixel_count, new_width))
        return ascii_string

    def convert(self, convert_to_image: bool, new_width: int = 200, save: bool = False, colorness=True) -> None:
        """
        Converts an image depending on the parameters of function.
        :param convert_to_image: True - converts to image. False - converts to string.
        :param new_width: Width of Processed  Image.
        :param save: True - saves converted image. False - doesn't save converted image(for video).
        :param colorness: True - gives color to characters. False - characters will be in 182, 183, 183.
        """
        if convert_to_image:
            return self.convertToColor(new_width, colorness=colorness, save=save)
        else:
            ascii_str = self.convertToString(new_width)
            file_name = self.path.split('/')[-1].split('.')[0]
            with open(f"{"/".join(self.path.split('/')[:-1])}/{file_name}.txt", 'w') as f:
                f.write(ascii_str)

    @staticmethod
    def resizeImage(image: Image, newWidth: int) -> Image:
        """
        Counts ratio of height/width and converts image using new width.
        :param image: Pillow image.
        :param newWidth: Width of processed image.
        :return: returns Resized image.
        """
        width, height = image.size
        factor = height / width
        newHeight = int(factor * newWidth)

        return image.resize((newWidth, newHeight))

    def convertToColor(self, new_width: int = 200, font_size: int = 16, background: tuple = (40, 44, 52),
                       colorness: bool = True, save: bool = False) -> Image:
        """
        Ascii character to image converter.
        :param new_width: Width of processed image.
        :param font_size: Size of character in image.
        :param background: Background color in RGB format.
        :param colorness: True - converts using colored characters. False - converts using gray characters.
        :param save: True - saves an image. False - only returns PIL.Image.
        :return: Pillow Image.
        """
        # Resizing original image.
        originalImage = Image.open(self.path).convert('RGB')
        originalImage = self.resizeImage(originalImage, new_width)

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
                    # Fills with standard color.
                    color = (182, 183, 183)

                draw.text((x * (font_size - 6), y * font_size), char, font=font, fill=color)

        if save:
            file_name = self.path.split('/')[-1].split('.')[0]
            image.save(f'{"/".join(self.path.split('/')[:-1])}/{file_name}-ascii.png')
        return image


if __name__ == '__main__':
    file_path = f"{os.getenv('folder_path')}/TestImages/1.png"
    a = Image2Ascii(file_path)
    a.convertToColor(200, colorness=True, save=True)
