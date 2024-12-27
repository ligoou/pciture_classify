# 这是一个示例 Python 脚本。
import os
import shutil
from datetime import datetime

from src import compress_image
from src.ExtractPhotoInfo import extract_timestamp
from src.ExtractVideoInfo import get_video_metadata
from src.compress_video import compress_video


def compress_file(input_dir, output_dir):
    """
    批量压缩视频文件，并根据元数据生成文件名。
    :param input_dir: 输入目录，包含待压缩视频
    :param output_dir: 输出目录，存储压缩后视频
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 用于跟踪文件名重复计数
    name_counter = {}

    for file_name in os.listdir(input_dir):
        input_file = os.path.join(input_dir, file_name)
        print(f"Processing {file_name}...")
       #压缩图片
        if not os.path.isfile(input_file) or  file_name.lower().endswith(('.jpg','.png','.jpeg','.webp','.tiff')):
            image_create_time = extract_timestamp(input_file)
            if image_create_time is None:
                image_create_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 如果无元数据，用当前时间代替

            # 生成唯一文件名
            if image_create_time not in name_counter:
                name_counter[image_create_time] = 0
            else:
                name_counter[image_create_time] += 1
            output_file_name = f"{image_create_time}_{name_counter[image_create_time]}.webp"
            output_file = os.path.join(output_dir, output_file_name)
            compress_image.compress_image_to_webp(input_file, output_file, quality=85)
            print(f"Compressed {file_name} -> {output_file}")
            continue


        # 支持的视频格式扩展名
        if not os.path.isfile(input_file) or not file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.mov','.heic')):
            output_file = os.path.join(output_dir, file_name)
            shutil.copy(input_file, output_file)
            print(f"Copied {file_name} -> {output_file}")
            continue

        video_create_time = get_video_metadata(input_file)
        if video_create_time is None:
            video_create_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 如果无元数据，用当前时间代替

        # 生成唯一文件名
        if video_create_time not in name_counter:
            name_counter[video_create_time] = 0
        else:
            name_counter[video_create_time] += 1

        #视频
        output_file_name = f"{video_create_time}_{name_counter[video_create_time]}.mp4"
        output_file = os.path.join(output_dir, output_file_name)

        try:
            compress_video(input_file, output_file, crf=23, preset="fast", codec="libx264")

            print(f"Compressed {file_name} -> {output_file}")
        except Exception as e:
            print(f"Error compressing {file_name}: {e}")


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    compress_file('d:\\z_in', 'd:\\z_output')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
