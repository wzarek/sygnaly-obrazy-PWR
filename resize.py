import numpy as np
from PIL import Image
from scipy.interpolate import interp2d, RegularGridInterpolator, interpn
import time

def resize(image, scale, name, interp: str):
    start_time = time.time()

    original_height, original_width = image.shape[:2]

    new_height, new_width = int(original_height * scale), int(original_width * scale)
    new_image = np.empty((new_height, new_width, 3), dtype=np.uint8)

    x_coords = np.linspace(0, original_width - 1, new_width)
    y_coords = np.linspace(0, original_height - 1, new_height)
    xv, yv = np.meshgrid(x_coords, y_coords)

    new_red = interpn((np.arange(original_width), np.arange(original_height)), image[:,:,0], (xv, yv), method=interp)
    new_green = interpn((np.arange(original_width), np.arange(original_height)), image[:,:,1], (xv, yv), method=interp)
    new_blue = interpn((np.arange(original_width), np.arange(original_height)), image[:,:,2], (xv, yv), method=interp)

    new_image[:,:,0] = new_red
    new_image[:,:,1] = new_green
    new_image[:,:,2] = new_blue

    resizedImg = Image.fromarray(new_image)
    resizedImg.save(f'resize-rotate/{name}-{interp}.jpg')

    stop_time = time.time()
    elapsed_time = stop_time - start_time

    return new_image, elapsed_time

def main():
    image = np.array(Image.open('Leopard-1.jpg'))
    interp_methods = ['nearest', 'linear', 'cubic']

    for method in interp_methods:
        resized, elapsed_time = resize(image, 0.5, 'res-0_5', method)
        a, elapsed_time_2 = resize(resized, 2, 'res-1', method)
        mse = (np.square(image - a)).mean(axis=None)
        print(f'{method}, time for downscaling and upscaling: {elapsed_time + elapsed_time_2} seconds, MSE = {mse}')

if __name__ == '__main__':
    main()
