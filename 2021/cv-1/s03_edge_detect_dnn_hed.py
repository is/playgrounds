"""
https://cloud.tencent.com/developer/article/1445963

https://github.com/s9xie/hed
https://github.com/ashukid/hed-edge-detector

pretraind model:
http://vcl.ucsd.edu/hed/hed_pretrained_bsds.caffemodel
https://github.com/ashukid/hed-edge-detector/raw/master/hed_pretrained_bsds.caffemodel
"""
import cv2 as cv
import numpy as np
import argparse

# 自定义层
class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0

    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]

        self.ystart = (inputShape[2] - targetShape[2]) // 2
        self.xstart = (inputShape[3] - targetShape[3]) // 2
        self.yend = self.ystart + height
        self.xend = self.xstart + width
        return [[batchSize, numChannels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:,:,self.ystart:self.yend,self.xstart:self.xend]]


def init_network():
    cv.dnn_registerLayer('Crop', CropLayer)
    net = cv.dnn.readNet(
        'hed/deploy.prototxt',
        "hed/hed_pretrained_bsds.caffemodel")
    return net

def main():
    parser = argparse.ArgumentParser(
        description='Code for Canny Edge Detector tutorial.')
    parser.add_argument(
        '--input', help='Path to input image.',
        default='s/02__source.jpg')
    args = parser.parse_args()
    src = cv.imread(cv.samples.findFile(args.input))
    if src is None:
        print('Could not open or find the image: ', args.input)
        exit(0)

    net = init_network()
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    inp = cv.dnn.blobFromImage(src, 
        scalefactor=1.0,
        mean=(104.00698793, 116.66876762, 122.67891434),
        swapRB=False, crop=False)
    net.setInput(inp)
    out = net.forward()
    print(out.shape)
    out = out[0,0]
    out = ((1 - out) * 255).astype(np.uint8)
    cv.imwrite('s/02__edge_detect_dnn_hed.jpg', out)
    print(np.max(out))

if __name__ == '__main__':
    main()