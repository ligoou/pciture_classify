import os
from datetime import datetime
import subprocess
import json
import shutil

import compress_image


from ffmpeg import FFmpeg

from src.ExtractVideoInfo import get_video_metadata


def compress_video(input_path, output_path, crf=23, preset="slow", codec="libx264"):
    """
    使用 ffmpeg-python 库压缩视频。

    :param input_path: 输入视频文件路径
    :param output_path: 输出视频文件路径
    :param crf: 恒定质量因子 (推荐值 18-28，值越高压缩越大，画质越低)
    :param preset: 压缩预设 (ultrafast, superfast, faster, fast, medium, slow, slower, veryslow)
    :param codec: 编码器 (如 "libx264" 或 "libx265" 用于 H.264 和 H.265)
    """

    ffmpeg  = FFmpeg().input(input_path)
    ffmpeg \
    .output(output_path, vcodec=codec, crf=crf, preset=preset, movflags="+faststart") \
    .execute()
    print(f"Compressed video saved to {output_path}")
