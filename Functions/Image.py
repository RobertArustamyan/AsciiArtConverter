from PIL import Image
from abc import ABC
import os
from dotenv import load_dotenv
from Functions.Characters import get_value

# Loading .env file data
load_dotenv()


class ImageWork(ABC):
    def __init__(self, image_url: str):
        try:
            self.img = Image.open(image_url)
            if image_url.endswith('.png'):
                self.img = self.img.convert('RGB')
            self.name = image_url.split('/')[-1].split('.')[0]
        except FileNotFoundError:
            print("The file wasn't able to load")
        self._width, self._height = self.img.size
        self._pixels = self.img.load()


class GrayImage(ImageWork):
    def convert_to_gray(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                r, g, b = self._pixels[x, y]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                self._pixels[x, y] = (gray, gray, gray)

        self.img.save(f"../TestImages/{self.name}gray.jpg")


class ConvertImage(ImageWork):
    def _average_block_brightness(self, x, y, block_size) -> int:
        total_brightness = 0
        count = 0
        for i in range(y, min(self._height, y + block_size)):
            for j in range(x, min(self._width, x + block_size)):
                g1, _, _ = self._pixels[j, i]
                total_brightness += (255 - g1)
                count += 1
        return total_brightness // count if count > 0 else 0

    def _image_to_ascii(self, block_size) -> str:
        result = ''
        for y in range(0, self._height, block_size):
            for x in range(0, self._width, block_size):
                pixel_brightness = self._average_block_brightness(x, y, block_size)
                char = get_value(pixel_brightness)
                result += char
            result += '\n'
        return result

    def get_image(self, block_size=10):
        result = self._image_to_ascii(block_size)
        file_name = f"{self.name}-ascii-{block_size}.txt"
        with open(f'../TestImages/{file_name}', 'w') as f:
            f.write(result)
        print(f"File with name {file_name}.txt is ready!")


def ascii_image(folder_path, file_name, file_format):
    gray = GrayImage(f'{folder_path}/TestImages/{file_name}.{file_format}')
    gray.convert_to_gray()
    ascii_im = ConvertImage(f'{folder_path}/TestImages/{file_name}gray.jpg')
    ascii_im.get_image(5)
    # Deleting filegray picture after ascii creating
    if os.path.exists(f'{folder_path}/TestImages/{file_name}gray.jpg'):
        os.remove(f'{folder_path}/TestImages/{file_name}gray.jpg')


if __name__ == "__main__":
    # Getting path from .env
    folder_path = os.getenv("folder_path")
    '''For making picture Gray'''
    # I = GrayImage(f'{folder_path}/TestImages/saturn.png')
    # I.convert_to_gray()

    # C = ConvertImage(f'{folder_path}/TestImages/saturngray.jpg')
    # C.get_image(5)
    ascii_image(folder_path, 'test', 'jpg')
