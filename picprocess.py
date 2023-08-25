import cv2
import numpy as np
import random
import os

def preprocess_image(image_path):
    # 读取图片
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    # 判断是否为正方形
    height, width, _ = image.shape
    if height != width:
        # 裁剪为正方形
        size = min(height, width)
        image = image[0:size, 0:size]
    
    # 裁剪成32x32块
    tiles = []
    tile_size = 32
    for i in range(0, image.shape[0], tile_size):
        for j in range(0, image.shape[1], tile_size):
            tile = image[i:i+tile_size, j:j+tile_size]
            tiles.append(tile)
    
    # 随机打乱位置
    random.shuffle(tiles)
    
    # 添加高斯模糊
    blurred_tiles = []
    for tile in tiles:
        blurred_tile = cv2.GaussianBlur(tile, (5, 5), 0)
        blurred_tiles.append(blurred_tile)
    
    # 创建输出文件夹
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # 输出处理后的图片
    for i, tile in enumerate(blurred_tiles):
        output_path = f"{output_folder}/{i}.jpg"
        cv2.imencode('.jpg', tile)[1].tofile(output_path)
    
    print("处理完成！")

# 输入图片路径（包含中文路径）
image_path = input("请输入图片路径：").encode('utf-8').decode('utf-8')

# 预处理图片
preprocess_image(image_path)
