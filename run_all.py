import os
from mutagen.flac import FLAC
import cv2
import numpy as np
import random
from mutagen import File
from PIL import Image, ImageFilter

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

def extract_cover_image_mp3(file_path):
	audio = File(file_path)
	if audio is None:
		return None
	if 'APIC:' in audio.tags:
		# 提取封面图片数据
		cover_data = audio.tags['APIC:'].data
		# 将封面图片数据保存为文件
		cover_file_path = os.path.splitext(file_path)[0] + '.jpg'
		with open(cover_file_path, 'wb') as cover_file:
			cover_file.write(cover_data)
		return cover_file_path

	return None
	

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

def merge_images():
	# 创建一个空白的512x512图片，填充为黑色
	output_image = Image.new('RGB', (512, 512), (0, 0, 0))
	count = 0
	used_nums = []

	for _ in range(256):
		if count == 256:
			break

		# 尝试5次随机选择图片块
		for _ in range(5):
			num = random.randint(0, 255)
			# 如果这个数字已经用过5次，则继续尝试
			if used_nums.count(num) >= 5:
				continue

			used_nums.append(num)
			filename = f'output/{num}.jpg'
			if os.path.exists(filename):
				image = Image.open(filename)
				image = image.resize((32, 32))
				x = (count % 16) * 32
				y = (count // 16) * 32
				output_image.paste(image, (x, y))
				count += 1
				break
		else:
			# 如果尝试5次都没有取到合适的随机数，则随机选取一个0-255的整数
			while True:
				num = random.randint(0, 255)
				if used_nums.count(num) < 5:
					used_nums.append(num)
					filename = f'output/{num}.jpg'
					if os.path.exists(filename):
						image = Image.open(filename)
						image = image.resize((32, 32))
						x = (count % 16) * 32
						y = (count // 16) * 32
						output_image.paste(image, (x, y))
						count += 1
					break

	# 对整个拼接图像进行高斯模糊处理
	output_image = output_image.filter(ImageFilter.GaussianBlur(radius=45))

	output_image.save('merged_image.jpg')
	

file_path = input("请输入mp3文件或flac文件路径：") 
file_path_1 = file_path

file_name, file_extension = os.path.splitext(file_path_1)
file_extension = file_extension.lower()
file_extension = file_extension.strip()
print("file_extension=" + '"' + file_extension + '"')
if file_extension == ".flac":
	cover_image_path = extract_cover_image(file_path)
	if cover_image_path:
		print(f'封面图片已提取，并保存为：{cover_image_path}')
	else:
		print('该文件没有封面图片。')
if file_extension == ".mp3":
	cover_image_path = extract_cover_image_mp3(file_path)
	if cover_image_path:
		print(f'封面图片已提取，并保存为：{cover_image_path}')
	else:
		print('该文件没有封面图片。')

#获取图片路径
image_path = f'{cover_image_path}'.encode('utf-8').decode('utf-8')
#裁剪图片并打乱
preprocess_image(image_path)
#拼接图片
merge_images()
