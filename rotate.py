import numpy as np
import cv2


def rotate(image, angle):
    (height, width) = image.shape[:2]
    center = (width / 2, height / 2)

    rotated_image = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, rotated_image, (width, height))

    cv2.imwrite(f'resize-rotate/rotated-{angle}.jpg', rotated_image)


def main():
    image = cv2.imread('Leopard-1.jpg')
    rotate(image, 45)


if __name__ == '__main__':
    main()
