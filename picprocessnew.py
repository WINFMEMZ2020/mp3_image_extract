from PIL import Image, ImageFilter
import os
import random

# 拼接图片
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
    output_image = output_image.filter(ImageFilter.GaussianBlur(radius=2))

    output_image.save('merged_image.jpg')

merge_images()
