import os
import h5py
import numpy as np
from PIL import Image
import sys
Image.MAX_IMAGE_PIXELS = None

CX, CY, CZ = 256, 256, 256

input_image_folder = sys.argv[1]
output_cube_folder = sys.argv[2]
output_cube_subfolder_format = 'section_{}_to_{}'


assert os.path.isdir(input_image_folder), 'Input folder does not exist!'
if not os.path.exists(output_cube_folder):
    os.mkdir(output_cube_folder)

input_image_files = sorted([os.path.join(input_image_folder, x) for x in os.listdir(input_image_folder)])

(MX, MY), MZ = np.asarray(Image.open(input_image_files[0]), dtype=np.uint16).shape, len(input_image_files)
print('Input image stack size:', MX, MY, MZ)

def load_16bit_image(image_path):
    temp = np.asarray(Image.open(image_path), dtype=np.uint16)
    minv, maxv = 0., np.amax(temp)
    temp = (temp - minv) * 255 / maxv
    temp = temp.astype(np.uint8)
    return temp


def load_stack(start_z, image_files):
    this_images = image_files[start_z:min(MZ, start_z + CZ)]
    mat = []
    for image_path in this_images:
        loaded_img = load_16bit_image(image_path)
        mat.append(loaded_img)
    return np.array(mat)


def output_cube(data, output_path):
    out = h5py.File(output_path, 'w')
    out.create_dataset('raw', data=data)


if __name__ == '__main__':
    cnt = 0
    for SZ in range(0, MZ, CZ):
        entire_image_stack = load_stack(SZ, input_image_files)
        output_sub_folder = os.path.join(output_cube_folder, output_cube_subfolder_format.format(SZ, min(MZ - 1, SZ + CZ - 1)))
        if not os.path.exists(output_sub_folder):
            os.mkdir(output_sub_folder)
        for SX in range(0, MX, CX):
            for SY in range(0, MY, CY):
                this_cube = entire_image_stack[:,SX:min(MX, SX+CX), SY:min(MY, SY+CY)]
                print(f'Cube {cnt}, starting_position: Z = {SZ}, X = {SX}, Y = {SY}, and size = {this_cube.shape}')
                sys.stdout.flush()
                output_path = os.path.join(output_sub_folder, f'Z{SZ}_X{SX}_Y{SY}.h5')
                output_cube(this_cube, output_path)
                # f = h5py.File(output_path, 'r')
                # print(np.allclose(this_cube, f['raw'][:]))
                cnt += 1





