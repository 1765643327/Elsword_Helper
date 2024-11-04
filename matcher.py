import cv2
import numpy as np


def letterbox_resize(image, target_size):
    # 获取目标宽度和高度
    target_width, target_height = target_size
    original_height, original_width = image.shape[:2]

    # 计算缩放比例
    scale = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # 缩放图像
    resized_image = cv2.resize(image, (new_width, new_height))

    # 创建一个填充的图像
    new_image = np.full((target_height, target_width, 3),
                        0, dtype=np.uint8)  # 使用灰色填充

    # 计算填充的偏移量
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    # 将缩放后的图像放置到填充的图像中间
    new_image[y_offset:y_offset + new_height,
              x_offset:x_offset + new_width] = resized_image

    return new_image


def template_matching(image_path, template_path):
    # 读取图像和模板
    image = cv2.imread(image_path)
    template = cv2.imread(template_path)

    # 将图像和模板转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 对灰度图像进行二值化
    _, binary_image = cv2.threshold(
        gray_image, 65, 255, cv2.THRESH_BINARY_INV)
    _, binary_template = cv2.threshold(
        gray_template, 65, 255, cv2.THRESH_BINARY_INV)

    # 获取模板的宽度和高度
    template_height, template_width = binary_template.shape[:2]

    # 执行模板匹配
    result = cv2.matchTemplate(
        binary_image, binary_template, cv2.TM_CCORR_NORMED
    )

    # 设置阈值来判断匹配程度
    threshold = 0.97
    y_indexes, x_indexes = np.where(result >= threshold)

    # 绘制矩形框框出匹配位置
    for (x, y) in zip(x_indexes, y_indexes):
        cv2.rectangle(image, (x, y), (x + template_width,
                      y + template_height), (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Template Matching', image)
    cv2.imshow('Binary Image', binary_image)
    cv2.imshow('Binary Template', binary_template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_path = '/home/zk/图片/image_1.jpg'
    template_path = '/home/zk/图片/1.jpg'
    template_matching(image_path, template_path)
