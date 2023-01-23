import cv2
import numpy as np
from PIL import Image
from scipy.interpolate import interp2d, RegularGridInterpolator, interpn
import time


def resizecv(image, scale, name, interp):
    start_time = time.time()

    new_height, new_width = int(image.shape[0] * scale), int(image.shape[1] * scale)
    if interp == 'nearest':
        new_image = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_NEAREST)
    elif interp == 'linear':
        new_image = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_LINEAR)
    elif interp == 'cubic':
        new_image = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_CUBIC)

    cv2.imwrite(f'resize-rotate/{name}-{interp}.jpg', new_image)

    stop_time = time.time()
    elapsed_time = stop_time - start_time

    return new_image, elapsed_time


def resize(image, scale, name, interp: str):
    start_time = time.time()

    original_height, original_width = image.shape[:2]

    new_height, new_width = int(original_height * scale), int(original_width * scale)

    x_coords = np.linspace(0, original_width - 1, new_width)
    y_coords = np.linspace(0, original_height - 1, new_height)
    xv, yv = np.meshgrid(x_coords, y_coords)

    new_image = interpn((np.arange(original_width), np.arange(original_height)), image, (xv, yv), method=interp)

    resizedImg = Image.fromarray(new_image.astype(np.uint8))
    resizedImg.save(f'resize-rotate/{name}-{interp}.jpg')

    stop_time = time.time()
    elapsed_time = stop_time - start_time

    return new_image, elapsed_time


def main():
    image = np.array(Image.open('Leopard-1.jpg'))
    interp_methods = ['nearest', 'linear', 'cubic']

    for method in interp_methods:
        resized, elapsed_time = resizecv(image, 0.5, 'res-0_5', method)
        a, elapsed_time_2 = resizecv(resized, 2, 'res-1', method)
        mse = (np.square(image - a)).mean(axis=None)
        print(f'{method}, time for downscaling and upscaling: {elapsed_time + elapsed_time_2} seconds, MSE = {mse}')


if __name__ == '__main__':
    main()
