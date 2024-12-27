import json
import subprocess
from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


def get_gps_from_mp4(file_path):
    parser = createParser(file_path)
    metadata = extractMetadata(parser)

    if metadata:
        for line in metadata.exportPlaintext():
            print(f"line: {line}")
            if 'GPS' in line or 'Location' in line:
                print(line)


from pymediainfo import MediaInfo


def extract_gps_from_mp4(file_path):
    media_info = MediaInfo.parse(file_path)
    gps_data = {}

    for track in media_info.tracks:
        if track.track_type == "General" or track.track_type == "Video":
            if hasattr(track, 'location'):
                gps_data['location'] = track.location
            if hasattr(track, 'other_location'):
                gps_data['other_location'] = track.other_location

    return gps_data

def get_video_metadata(input_path):
    """
    获取视频的拍摄时间元数据（使用 ffprobe 提取）。

    :param input_path: 视频文件路径
    :return: 拍摄时间字符串 (格式: YYYYMMDD_HHMMSS)，如果没有元数据则返回 None
    """
    try:
        # 使用 ffprobe 提取视频创建时间
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_entries", "format_tags=creation_time",
            input_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        metadata = json.loads(result.stdout)

        # 提取 creation_time 信息
        creation_time = metadata.get("format", {}).get("tags", {}).get("creation_time")
        if creation_time:
            # 转换时间格式为 YYYYMMDD_HHMMSS
            dt = datetime.fromisoformat(creation_time.replace("Z", ""))
            return dt.strftime("%Y%m%d_%H%M%S")
        return None
    except Exception as e:
        print(f"Error reading metadata for {input_path}: {e}")
        return None
