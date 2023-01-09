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
    # Create a blank image with the same size as the frame
    modified_frame = deepcopy(frame)
    j = 0
    for segment in saved_segments:
        modified_frame.paste(segment, (0, j))
        j += row_interval

    # Set the number of rows to copy from the frame and the interval between rows
    row_interval = 10

    # Create a blank image with the same size as the frame
    segment = Image.new('RGB', size=(frame.size[0], row_interval))
    # Copy the rows onto the blank image
    box = (0, i, frame.size[0], i + row_interval)
    region = frame.crop(box)
    segment.paste(region)
    saved_segments.append(segment)
    modified_frame.paste(segment, (0, i))
    i += row_interval
    # Add the modified frame to the list of modified frames
    modified_frames.append(modified_frame)

# Save the modified frames as a GIF
modified_frames[0].save('aliasing/output.gif', format='gif', save_all=True, append_images=modified_frames[1:], duration=100)