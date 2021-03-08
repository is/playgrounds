import rawpy
import cv2
import glob
import os
import sys

files = glob.glob(sys.argv[1]+'*.ARW')
num_photos = len(files)
print ('nr ARW founded --> ' + str(num_photos))

if num_photos > 0:

    if not os.path.exists(sys.argv[1] + 'converted/'):
        os.makedirs(sys.argv[1] + 'converted/')

    for f in files:
        print ('Processing --> ' + f)
        with rawpy.imread(f) as raw:
            rgb16 = raw.postprocess(output_bps=16, half_size=True)
            rgb = raw.postprocess(half_size=True)
            print(rgb.dtype)
            print(rgb16.dtype)
            print(rgb16.shape)
            print(raw.raw_image.shape)
            print(raw.raw_image.dtype)
            for i in range(30):
                print("%d %d %d %d" % (
                    i, rgb[100 + i, 100 + i, 2], 
                    rgb16[100 + i, 100 + i, 2],
                    raw.raw_image[(100 + i)*2, (100 + i)*2]))
            # fileName = os.path.splitext(f)[0] + '.png'
            # fileName = fileName.replace(sys.argv[1], '')
            # cv2.imwrite(fileName, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR),
            #     [cv2.IMWRITE_PNG_COMPRESSION, 9])

print('Conversion finished')

