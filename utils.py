from consts import BitmapType

class NumberUtils:
    @classmethod
    def round_pixels_20(cls, pixels):
        return round(pixels * 100) / 100

    @classmethod
    def round_pixels_400(cls, pixels):
        return round(pixels * 10000) / 10000

class ColorUtils:
    @classmethod
    def alpha(cls, color):
        return int((color >> 24) & 0xff) / 255.0

    @classmethod
    def rgb(cls, color):
        return (color & 0xffffff)

    @classmethod
    def to_rgb_string(cls, color):
        c = "{:06x}".format(color & 0xffffff)
        return f"#{c}"

class ImageUtils:
    @classmethod
    def get_image_size(cls, data):
        pass

    @classmethod
    def get_image_type(cls, data):
        pos = data.tell()
        image_type = 0
        data.seek(0, 2)  # 移动文件指针到最终位置
        if data.tell() > 8:
            data.seek(0)
            header = data.read(8)
            if header.startswith(b'\xff\xd8'):
                image_type = BitmapType.JPEG
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):
                image_type = BitmapType.PNG
            elif header.startswith(b'GIF89a'):
                image_type = BitmapType.GIF89A
        data.seek(pos)
        return image_type