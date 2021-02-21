import rawpy
import exifread


FN = "_DSC0035-startrails.ARW"
#FN = 'DSC01789.ARW'
raw = rawpy.imread(FN)
thumb = raw.extract_thumb()
with open('thumb.jpg', 'wb') as f:
    f.write(thumb.data)
print(raw.raw_type)
print(raw.sizes)
print(raw.num_colors)
print(raw.color_desc.decode('utf-8'))

raw_image = raw.raw_image.copy()
print(raw_image.shape)
print(raw_image.dtype)
print(raw.raw_value(4000, 3001))
# print(raw.color_matrix)

with open(FN, 'rb') as fin:
    exif_file = exifread.process_file(fin, details=False, strict=True)
for key, value in exif_file.items():
    print(f"{key}: {value}")



"""
files = glob.glob(sys.argv[1]+'*.ARW')
num_photos = len(files)
print ('nr ARW founded --> ' + str(num_photos))

if num_photos > 0:

    if not os.path.exists(sys.argv[1] + 'converted/'):
        os.makedirs(sys.argv[1] + 'converted/')

    for f in files:
        print ('Processing --> ' + f)
        with rawpy.imread(f) as raw:
            rgb = raw.postprocess()
        fileName = os.path.splitext(f)[0] + '.jpg'
        fileName = fileName.replace(sys.argv[1],'')
        newFileName = sys.argv[1] + 'converted/' + fileName
        imageio.imsave(newFileName, rgb)

print('Conversion finished')
"""
