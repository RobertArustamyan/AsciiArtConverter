import argparse
import sys
from Functions.Image import Image2Ascii
from dotenv import load_dotenv
import os
from Functions.Video import Video2Ascii

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        prog='Ascii Converter',
        description='Program converts (images, videos) to ascii (image, video, text)',
        epilog='Example usage: python main.py'
    )
    parser.add_argument('filename', type=str, help='Name of the file')
    parser.add_argument('new_width', type=int, help='New width of convert object')
    parser.add_argument('-s', '--string', action='store_true', help='If set, converts to string')
    parser.add_argument('-i', '--image', action='store_true', help='If set, converts to image')
    parser.add_argument('-v', '--video', action='store_true', help='If set, converts to video')

    args = parser.parse_args()
    filename = args.filename
    print(filename)
    if filename.endswith('.mp4'):
        if not args.video:
            print('Error: For video files, only the --video option is allowed')
            sys.exit(1)
        else:
            # Converts Video to Ascii Video
            path = f"{os.getenv('folder_path')}/TestVideos/{filename}"
            converter = Video2Ascii(path)
            fps = int(input("Fps for video: "))
            converter.convertVideo(fps=fps, new_width=args.new_width)

    elif filename.endswith('.png') or filename.endswith('.jpg'):
        if args.string or args.image:
            path = f"{os.getenv('folder_path')}/TestImages/{filename}"
            converter = Image2Ascii(path)
            if args.string:
                # Converts image into Ascii String
                converter.convert(convert_to_image=False, new_width=args.new_width)
            else:
                # Converts image into Ascii image
                converter.convert(convert_to_image=True, new_width=args.new_width)
        else:
            print('Error: For image files, only --string and --image is allowed')
            sys.exit(1)

    else:
        print('Error: File type is not supported. Please provide a .mp4, .png or .jpg format file.')
        sys.exit(1)


if __name__ == "__main__":
    main()
