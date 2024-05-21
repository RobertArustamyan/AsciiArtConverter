def get_dictionary() -> dict:
    gray_scale = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    return {len(gray_scale) - i: gray_scale[i] for i in range(len(gray_scale))}


def get_value(number) -> str:
    return get_dictionary()[number]


if __name__ == "__main__":
    print(get_value(64))
