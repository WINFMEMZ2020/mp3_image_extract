from PIL import Image, ImageFilter
import os

# 拼接图片
def merge_images():
    # 创建一个空白的512x512图片，填充为黑色
    output_image = Image.new('RGB', (512, 512), (0, 0, 0))
    count = 0

    for i in range(256):
        if count == 256:
            break

        filename = f'output/{i}.jpg'
        if os.path.exists(filename):
            image = Image.open(filename)
            image = image.resize((32, 32))
            x = (count % 16) * 32
            y = (count // 16) * 32
            output_image.paste(image, (x, y))
            count += 1

    # 对整个拼接图像进行高斯模糊处理
    output_image = output_image.filter(ImageFilter.GaussianBlur(radius=30))

    output_image.save('merged_image.jpg')

merge_images()
