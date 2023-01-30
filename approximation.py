import numpy as np
from PIL import Image
import cv2


def box(size):
    return np.ones((size, size)) * (1 / size ** 2)


def gaussian(size, sigma = 2):
    center = size // 2
    kernel = np.array([[np.exp(-((x - center) ** 2 + (y - center) ** 2) / (2 * sigma ** 2)) for x in range(size)] for y in range(size)])

    return kernel / np.sum(kernel)


def median_filter(img, size):
    img = np.array(img)
    height, width = img.shape[0:2]
    filtered = np.zeros_like(img)
    radius = size // 2
    padded = cv2.copyMakeBorder(img, radius, radius, radius, radius, cv2.BORDER_REPLICATE)

    for x in range(height):
        for y in range(width):
            for color in range(3):
                filtered[x, y, color] = np.median(padded[x:x + size, y:y + size, color].flatten())

    filtered = Image.fromarray(filtered)
    return filtered


def convolution_filter(img, kernel):
    img = np.array(img)
    height, width = img.shape[0:2]
    filtered = np.zeros_like(img)
    radius = kernel.shape[0] // 2
    padded = cv2.copyMakeBorder(img, radius, radius, radius, radius,
                                cv2.BORDER_REPLICATE)
    for x in range(height):
        for y in range(width):
            for color in range(3):
                filtered[x, y, color] = np.sum(padded[x:x + kernel.shape[0], y:y + kernel.shape[0], color] * kernel)

    filtered = Image.fromarray(filtered)
    return filtered


def main():
    img = Image.open('Leopard-with-noise.jpg')
    filter_types = ['box', 'gaussian', 'median']

    for method in filter_types:
        if method == 'median':
            result = median_filter(img, 10)
        elif method == 'box':
            result = convolution_filter(img, box(10))
        else:
            result = convolution_filter(img, gaussian(10))
        mse = (np.square(np.array(img) - np.array(result))).mean(axis=None)
        result.save(f"approximation/result-{method}.jpg")
        print(f'{method}, MSE = {mse}')


if __name__ == '__main__':
    main()
