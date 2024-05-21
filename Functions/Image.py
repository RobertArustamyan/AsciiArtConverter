from PIL import Image
import os
from dotenv import load_dotenv

# Loading .env file data
load_dotenv()


class ImageWork:
    def __init__(self, image_url: str):
        try:
            self.img = Image.open(image_url)
            self.name = image_url.split('/')[-1].split('.')[0]
        except FileNotFoundError:
            print("The file wasn't able to load")
        self._width, self._height = self.img.size
        self._pixels = self.img.load()

    def convert_to_gray(self):
        for y in range(self._height):
            for x in range(self._width):
                r, g, b = self._pixels[x, y]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                self._pixels[x, y] = (gray, gray, gray)

        self.img.save(f"../TestImages/{self.name}gray.jpg")


if __name__ == "__main__":
    # Getting path from .env
    folder_path = os.getenv("folder_path")

    I = ImageWork(f'{folder_path}/TestImages/3.jpg')
    I.convert_to_gray()
