import os
from mutagen.flac import FLAC

def extract_cover_image(file_path):
    audio = FLAC(file_path)
    if audio is None:
        return None

    if audio.pictures:
        # 提取封面图片数据
        cover_data = audio.pictures[0].data
        # 将封面图片数据保存为文件
        cover_file_path = os.path.splitext(file_path)[0] + '.jpg'
        with open(cover_file_path, 'wb') as cover_file:
            cover_file.write(cover_data)
        return cover_file_path

    return None

# 测试程序
file_path = r"C:\Users\WINFM\Music\RADWIMPS - スパークル (movie ver.).flac"  #替换为你的文件路径
cover_image_path = extract_cover_image(file_path)
if cover_image_path:
    print(f'封面图片已提取，并保存为：{cover_image_path}')
else:
    print('该文件没有封面图片。')
