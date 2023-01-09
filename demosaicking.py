from copy import deepcopy
import cv2
from PIL import Image

BAYER = [
    [1, 0],
    [2, 1]
]

XTRANS = [
    [1, 2, 0, 1, 0, 2],
    [0, 1, 1, 2, 1, 1],
    [2, 1, 1, 0, 1, 1],
    [1, 0, 2, 1, 2, 0],
    [2, 1, 1, 0, 1, 1],
    [0, 1, 1, 2, 1, 1]
]

def CFA(img, type):
    mask = BAYER if type == 'BAYER' else XTRANS

    out = deepcopy(img)
    for id, row in enumerate(out):
        for idx, col in enumerate(row):
            for index, channel in enumerate(col):
                if index != mask[id % len(mask)][idx % len(mask[id % len(mask)])]:
                    out[id][idx][index] = 0
    
    img2 = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img2)
    im_pil.save(f'demosaicking/{type}-mosaic.png')

    return img2

def interpolate(img, type, depth):
    out = deepcopy(img)
    for id, row in enumerate(out):
        for idx, col in enumerate(row):
            if sum(col) == 0:
                continue
            else:
                for index, channel in enumerate(col):
                    avg_arr = []
                    for i in range(1, depth+1):
                        if idx-i >= 0 and out[id][idx-i][index]:
                            avg_arr.append(out[id][idx-i][index])
                        if id-i >= 0 and idx-i >= 0 and out[id-i][idx-i][index]:
                            avg_arr.append(out[id-i][idx-i][index])
                        if id-i >= 0 and out[id-i][idx][index]:
                            avg_arr.append(out[id-i][idx][index])
                        if id+i < len(out) and idx >= 0 and out[id+i][idx-i][index]:
                            avg_arr.append(out[id+i][idx-i][index])
                        if id-i >= 0 and idx+i < len(out[id]) and out[id-i][idx+i][index]:
                            avg_arr.append(out[id-i][idx+i][index])
                        if id+i < len(out) and out[id+i][idx][index]:
                            avg_arr.append(out[id+i][idx][index])
                        if idx+i < len(out[id]) and out[id][idx+i][index]:
                            avg_arr.append(out[id][idx+i][index])
                        if id+i < len(out) and idx+i < len(out[id]) and out[id+i][idx+i][index]:
                            avg_arr.append(out[id+i][idx+i][index])
                        if len(avg_arr) >= depth:
                            break
                    out[id][idx][index] = sum(avg_arr) / len(avg_arr)

    img2 = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img2)
    im_pil.save(f'demosaicking/{type}-demosaic.png')

    return img2

def getDiff(img1, img2):
    diff = abs(img1 - img2)

    imgCV = cv2.cvtColor(diff, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(imgCV)
    im_pil.save(f'demosaicking/diff.png')

def main():
    img = cv2.imread('4demosaicking.bmp')
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # bayerCFA = CFA(img_rgb, 'BAYER')
    # bayerInterpolated = interpolate(bayerCFA, 'BAYER', 2)
    # getDiff(img_rgb, bayerInterpolated)
    xtransCFA = CFA(img_rgb, 'XTRANS')
    xtransInterpolated = interpolate(xtransCFA, 'XTRANS', 2)
    getDiff(img_rgb, xtransInterpolated)

if __name__ == '__main__':
    main()