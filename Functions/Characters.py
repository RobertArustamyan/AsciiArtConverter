def get_dictionary() -> dict:
    gray_scale = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    return {len(gray_scale) - i: gray_scale[i] for i in range(len(gray_scale))}


def get_value(number: int) -> str:
    scale_factor = 256 / 72
    index = number // scale_factor
    return ' ' if index == 0 else get_dictionary()[index]


if __name__ == "__main__":
    pass
