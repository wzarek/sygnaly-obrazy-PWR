from copy import deepcopy
from PIL import Image

gif = Image.open('aliasing/animation.gif')
frames = []
try:
    while True:
        frames.append(gif.copy())
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

modified_frames = []
saved_segments = []
i = 10
for frame in frames:
    modified_frame = deepcopy(frame)
    j = 0
    for segment in saved_segments:
        modified_frame.paste(segment, (0, j))
        j += row_interval

    row_interval = 8

    segment = Image.new('RGB', size=(frame.size[0], row_interval))
    box = (0, i, frame.size[0], i + row_interval)
    region = frame.crop(box)
    segment.paste(region)
    saved_segments.append(segment)
    modified_frame.paste(segment, (0, i))
    i += row_interval
    modified_frames.append(modified_frame)

modified_frames[0].save('aliasing/output.gif', format='gif', save_all=True, append_images=modified_frames[1:])