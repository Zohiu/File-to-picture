from PIL import Image
import zlib

image_file_path = input("Please input the file path : ")
output_file_path = "recovered-" + "".join(image_file_path.split("-pic.png")[:-1])

# Open the image
print("Opening image...")
image = Image.open(image_file_path)

# Get the pixel data from the image
print("Reading image data...")
pixels = list(image.getdata())

print("Reordering color values for conversion...")
# Extract RGB values from each pixel and add to a list
rgb_values = []
for pixel in pixels:
    r, g, b = pixel[:3]  # Extract RGB values
    rgb_values.append(r)
    rgb_values.append(g)
    rgb_values.append(b)


print("Converting color values to binary data...")
# Convert RGB values to binary data
binary_data = bytearray()
for i in range(0, len(rgb_values), 3):
    r = rgb_values[i]
    g = rgb_values[i+1]
    b = rgb_values[i+2]
    binary_data.extend(bytes([r, g, b]))

# Save the binary data as a file
with open(output_file_path, 'wb') as binary_file:
    print("Decompressing binary data...")
    decompressed_data = zlib.decompress(binary_data)
    print("Saving binary data to output file...")
    binary_file.write(decompressed_data)
    print(f"Output saved as {output_file_path}")