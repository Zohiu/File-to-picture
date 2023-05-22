from PIL import Image
import math
import zlib


def calculate_width_height(num_pixels, aspect_ratio):
    width_ratio, height_ratio = aspect_ratio
    total_ratio = width_ratio / height_ratio

    # Calculate the width and height based on the total number of pixels and aspect ratio
    width = int(math.sqrt(num_pixels * total_ratio))
    height = int(math.ceil(width / total_ratio))

    # Adjust width and height to match the total number of pixels
    while width * height < num_pixels:
        width += 1
        if width * height >= num_pixels:
            break
        height += 1

    return width, height


binary_file_path = input("Please input the file path : ")
image_file_path = f'{binary_file_path}-pic.png'

# Read the binary data from the file
with open(binary_file_path, 'rb') as binary_file:
    print("Reading file...")
    raw_data = binary_file.read()
    print(f"{len(raw_data)} bytes read.")
    print("Compressing file...")
    binary_data = zlib.compress(raw_data) # Can also remove compression, but it makes the png look cooler and also take less size.
    print(f"{len(binary_data)} compressed bytes.")

print("Converting bytes to color values...")
data_values = [int(bit) for byte in binary_data for bit in f"{byte:08b}"]
print("Reordering color values for usage...")
color_tuples = data_values

print("Running last tuple fix...")
# Check the size of the last tuple
# last_tuple = color_tuples[-1]
# last_tuple_size = len(last_tuple)

# Fill up the last tuple with 0s if the size is less than 3 to always have r, g and b present.
# if last_tuple_size < 3:
#     last_tuple += (0,) * (3 - last_tuple_size)
#     color_tuples[-1] = last_tuple

num_pixels = len(data_values)
print(f"{num_pixels} pixels required.")
aspect_ratio = (16, 9)  # Desired aspect ratio (width:height)
print(f"Choosing size of image with aspect ratio {aspect_ratio}...")

width, height = calculate_width_height(num_pixels, aspect_ratio)
print(f"Width: {width}, Height: {height}")
print(f"{width*height} total pixels.")

print("Creating image object...")
image = Image.new('RGB', (width, height))
index = 0

pixels = image.load()

print("Writing pixels...")
for y in range(height):
    for x in range(width):
        print(f"{index} out of {len(color_tuples) - 1} written. ({round((index / (len(color_tuples) - 1)) * 100)}%)", end="\r", flush=True)

        if index > len(color_tuples) - 1:
            r, g, b = (0, 0, 0)
            continue

        # print(color_tuples)
        if color_tuples[index] == 1:
            r, g, b, = 255, 255, 255
        else:
            r, g, b, = 0, 0, 0

        index += 1
        pixels[x, y] = (r, g, b)  # Set RGB values for the pixel

print(f"{index} out of {len(color_tuples) - 1} written. ({round((index / (len(color_tuples) - 1)) * 100)}%)")
print("Saving image file...")
image.save(image_file_path)
print(f"Output saved as {image_file_path}")