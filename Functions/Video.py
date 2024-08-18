import PIL.Image

from Functions.Image import Image2Ascii
from moviepy.editor import ImageSequenceClip, VideoFileClip
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()


class Video2Ascii:
    def __init__(self, path):
        self.path = path
        self.checkFile()

    def checkFile(self):
        """
        Checks the file existence
        :return: Expectation if file is not in necessary format.
        """
        try:
            file_extension = os.path.split(self.path)[1].lower().split('.')[1]
            if file_extension not in ['mp4']:
                raise FileNotFoundError
        except FileNotFoundError:
            print(f"The file provided is not in the necessary format")

    def extractFrames(self, fps: int = 5) -> list:
        """
        Gets frames from the video
        :param fps: Frames per second
        :return: Returns list of frames
        """
        clip = VideoFileClip(self.path)
        frames = [frame for frame in clip.iter_frames(fps)]
        clip.close()
        return frames

    @staticmethod
    def convertFrame(frame, new_width, colorness=True) -> PIL.Image:
        """
        Converts frame into PIL.Image.
        :param frame: One frame of the video.
        :param new_width: width of new video.
        """
        image = Image.fromarray(frame)
        temp_path = f"{os.getenv('folder_path')}/TestVideos/temp.png"
        image.save(temp_path)
        converter = Image2Ascii(temp_path)
        return converter.convert(convert_to_image=True, new_width=new_width, colorness=colorness, save=False)

    def convertVideo(self, fps: int = 5, new_width: int = 150) -> None:
        """
        Converts video depending on fps and desire width.
        :param fps: The amount of frames that will be get from 1 second of video.
        :param new_width: Width of converted video.
        """
        frames = self.extractFrames(fps)
        image_paths = []
        for i, frame in enumerate(frames):
            ascii_image = self.convertFrame(frame, new_width=new_width)
            image_path = f"{os.getenv('folder_path')}/TestVideos/frame_{i}.png"
            ascii_image.save(image_path)
            image_paths.append(image_path)
        clip = ImageSequenceClip(image_paths, fps=fps)
        file_name = self.path.split('/')[-1].split('.')[0]
        output_video_path = f"{os.getenv('folder_path')}/TestVideos/{file_name}-ascii.mp4"
        clip.write_videofile(output_video_path)
        for i in range(len(frames)):
            if os.path.exists(f"{os.getenv('folder_path')}/TestVideos/frame_{i}.png"):
                os.remove(f"{os.getenv('folder_path')}/TestVideos/frame_{i}.png")
        os.remove(f"{os.getenv('folder_path')}/TestVideos/temp.png")


if __name__ == "__main__":
    file_path = f"{os.getenv('folder_path')}/TestVideos/2.mp4"
    v = Video2Ascii(file_path)
    v.convertVideo(10)
