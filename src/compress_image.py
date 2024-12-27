import os
import time

import pillow_heif
from PIL import Image
from ffmpeg import FFmpeg

pillow_heif.register_heif_opener()

def compress_image_to_jpeg(input_path, output_path, quality=85, max_width=None):
    """
    压缩图片，同时尽量保持清晰度。

    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param quality: 图片质量 (1-100)
    :param max_width: 最大宽度（可选），超出则缩小
    """
    with Image.open(input_path) as img:
        # 调整图片分辨率
        if max_width and img.size[0] > max_width:
            width_percent = max_width / float(img.size[0])
            new_height = int(float(img.size[1]) * width_percent)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # 保存图片，设置优化选项
        img.save(output_path, format="JPEG", quality=quality, optimize=True)
        print(f"Compressed image saved at {output_path} with quality={quality}")


def compress_image_to_webp(input_path, output_path, quality=85):
    """
    压缩图片为 WebP 格式，同时尽量保持清晰度。

    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param quality: 图片质量 (1-100)
    """
    # 打开源图片
    with Image.open(input_path) as img:
        # 提取 EXIF 元数据（如果有）
        exif_data = img.info.get('exif')
        # 保存为 WebP 格式，同时保持元数据
        img.save(
            output_path, format="WEBP", quality=quality, optimize=True, exif=exif_data,
            method=6,  # 0-6, 0为默认，6为最慢但效果最好
            lossless=False,  # 是否无损压缩
            transparency=0,  # 0-255, 0为完全透明，255为完全不透明
            animation=0,  # 0-1, 0为不使用动画，1为使用
            minimize_size=True,  # 是否尽量减小文件大小
            alpha_compression=1,  # 0-1, 0为不压缩 alpha 通道，1为使用
            compression_level=4,  # 0-9, 0为最快，9为最慢
        )
        print(f"WebP image saved at {output_path} with quality={quality}")


from PIL import Image, ImageSequence
import pillow_heif

# 注册 HEIF 支持
pillow_heif.register_heif_opener()

# 打开 HEIF 文件
input_file = 'd:\\z_in\\IMG_1233.HEIC'
image = Image.open(input_file)
max_size = 2048
# 提取所有帧
frame_index = 0
for frame in ImageSequence.Iterator(image):
    original_size = (image.width, image.height)

    # 保存每一帧为图片
    if image.width > max_size or image.height > max_size:

        scale_factor = max_size / max(image.width, image.height)
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        frame = frame.resize((frame.width, frame.height), Image.Resampling.LANCZOS)
        print(f"调整分辨率: 原始尺寸 {original_size}, 调整后尺寸 {new_size}")
    else:
        print(f"无需调整分辨率: 当前尺寸 {original_size}")

    frame.save(f'd:\\z_in\\frame_{frame_index:04d}.WEBP',quality = 85, format="WEBP",  optimize=True,
            method=6,  # 0-6, 0为默认，6为最慢但效果最好
            lossless=False,  # 是否无损压缩
            transparency=0,  # 0-255, 0为完全透明，255为完全不透明
            animation=0,  # 0-1, 0为不使用动画，1为使用
            minimize_size=True,  # 是否尽量减小文件大小
            alpha_compression=1,  # 0-1, 0为不压缩 alpha 通道，1为使用
            compression_level=4,  # 0-9, 0为最快，9为最慢
        )
    os.utime(f'd:\\z_in\\frame_{frame_index:04d}.WEBP', (image.gettime(), time.time()))
    frame_index += 1

print(f"已提取 {frame_index} 帧并保存。")

