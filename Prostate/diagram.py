from skimage.io import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import rescale
from skimage.util import img_as_ubyte

#order of region centers is
# 0  1 | 6  7
# 2  3 | 8  9
# 4  5 | 10 11

IMAGES = [
    "req_pics/dotted_circle.png",
    "req_pics/one.png",
    "req_pics/two.png",
    "req_pics/three.png",
    "req_pics/four.png",
    "req_pics/five.png"
]
NUM_MASKS = [
    "req_pics/dotted_circle_mask.png",
    "req_pics/one_mask.png",
    "req_pics/two_mask.png",
    "req_pics/three_mask.png",
    "req_pics/four_mask.png",
    "req_pics/five_mask.png"
]

MASKS = [
    "req_pics/mask0.png",
    "req_pics/mask1.png",
    "req_pics/mask2.png",
    "req_pics/mask3.png",
    "req_pics/mask4.png",
    "req_pics/mask5.png",
    "req_pics/mask6.png",
    "req_pics/mask7.png",
    "req_pics/mask8.png",
    "req_pics/mask9.png",
    "req_pics/mask10.png",
    "req_pics/mask11.png",
    "req_pics/mask12.png"
]

#(row, col)
centers = [(158, 133), (166, 202), (225, 129), (229, 208), (290, 149), (302, 219), (166, 318), (153, 401), (236, 318), (221, 404), (301, 308), (292, 376)]

def withinDist(c1, c2, dist):
    return np.linalg.norm(c1-c2) < dist

def removeAlpha(im):
    ret = np.zeros((im.shape[0], im.shape[1], 3), dtype=im.dtype)
    for row in range(im.shape[0]):
        for col in range(im.shape[1]):
            ret[row, col][0] = im[row, col, 0]
            ret[row, col][1] = im[row, col, 1]
            ret[row, col][2] = im[row, col, 2]
    return ret

#draw sub image on image, given center (Default) or top left coord of subIm in im
def drawPatch(c, im, subIm, topLeft=False, mask=None):
    tl_x = c[1]
    tl_y = c[0]
    if not topLeft:
        tl_x -= subIm.shape[1]//2
        tl_y -= subIm.shape[0]//2
    for sub_y in range(subIm.shape[0]):
        for sub_x in range(subIm.shape[1]):
            x = sub_x + tl_x
            y = sub_y + tl_y
            masked_out = False
            if mask is not None:
                masked_out = mask[sub_y, sub_x].tolist() != [255, 255, 255] and mask[sub_y, sub_x].tolist() != 255 #account for 1 or 3 channel mask
            if x < 0 or x > im.shape[1]-1 or y < 0 or y > im.shape[0]-1 or masked_out:
                continue
            im[y, x] = subIm[sub_y, sub_x]

# overlays top on base (black pixels not overlayed)
def overlayImage(base, top):
    for row in range(base.shape[0]):
        for col in range(base.shape[1]):
            if top[row, col].tolist() == [0, 0, 0]:
                continue
            if np.linalg.norm(top[row, col]) < np.linalg.norm(base[row, col]): 
                base[row, col] = top[row, col]

def markupProstate(types, targeted):
    #read empty prostate
    im = imread("req_pics/sub_clean.png")
    im = removeAlpha(im)
    #extract subimage
    #row range, col range
    #subIm = im[495:896, 230:779] # indexing on empty.jpeg

    dots = imread("req_pics/dotted_background.png")
    #mask = imread("mask3.png")
    #mask = mask[..., np.newaxis]/255
    #mask = mask.astype(np.uint8)

    for i, target in enumerate(targeted):
        if target:
            mask = imread(MASKS[i])
            mask = (mask[..., np.newaxis]).astype(np.bool)
            maskedDots = dots * mask
            overlayImage(im, maskedDots)
   
    # put circles
    dotted = imread(IMAGES[0])
    #dotted = rescale(dotted, 0.5, order=3, channel_axis=2, preserve_range=True, anti_aliasing=True)

    for i, c in enumerate(centers):
        #if types[i] < 1 or types[i] > len(types) - 1:
        #    patch = dotted
        #    drawPatch(c, im, patch)
        #else:
        patch = imread(IMAGES[types[i]])
        mask = imread(NUM_MASKS[types[i]])
        drawPatch(c, im, patch, mask=mask)
    return im

def genDottedPat():
    dot = imread("req_pics/dot.png")
    dot = rescale(dot, 0.5, order=3, channel_axis=2, preserve_range=True, anti_aliasing=True).astype(np.uint8)
    rows = 401
    cols = 549
    step = dot.shape[0]
    dots = np.zeros((rows, cols, 3), dtype=np.uint8)
    for row in range(0, rows, step):
        for col in range(0, cols, step):
            drawPatch((row, col), dots, dot, topLeft=True)
    plt.imshow(dots)
    plt.show()
    imsave("req_pics/dotted_background.png", dots)

def genMask(inputName, maskName, color=[0,0,0], inv=False):
    im = imread(inputName)
    print(im)
    pat_mask = np.zeros((im.shape[0], im.shape[1]), dtype=np.bool)
    for row in range(im.shape[0]):
        for col in range(im.shape[1]):
            if not inv:
                pat_mask[row, col] = im[row, col].tolist() == color
            if inv:
                pat_mask[row, col] = im[row, col].tolist() != color
    plt.imshow(pat_mask)
    plt.show()
    imsave(maskName, img_as_ubyte(pat_mask))

def cleanNum(numIm, outName, thresh):
    im = imread(numIm)
    for row in range(im.shape[0]):
        for col in range(im.shape[1]):
            if withinDist(im[row, col], np.array([255, 255, 255]), thresh):
                im[row, col] = np.array([255, 255, 255])
    imsave(outName, im)

def workflow():
    # holds image we want to display at each position
    # ex want section 5 to be 1, do sections[5] = 1
    # sections are zero indexed
    types = np.zeros(len(centers), dtype=np.uint8)
    types[11] = 5
    types[10] = 4
    types[5] = 3
    types[3] = 2
    types[1] = 1
    #types[0] = 3
    targeted = np.zeros(len(centers), dtype=np.bool)
    targeted[3] = True
    targeted[1] = True
    targeted[0] = True
    pros = markupProstate(types, targeted)
    plt.imshow(pros)
    plt.show()
    imsave("sub_Ex_aa3.png", pros)

def rescaleIm(im):
    return rescale(im, 0.5, order=3, channel_axis=2, preserve_range=True, anti_aliasing=True).astype(np.uint8)

def main():
    # make masks for 3, 2, 1, then fill in masks for 4 and 5, and then should be good, then just need to make masks for othere 9 compartments
    #cleanNum("dotted_circle_small.png", "dotted_circle.png", 80)
    #genMask("dotted_circle.png", "dotted_circle_mask.png", color=[255, 255, 255], inv=True)
    
    workflow()
    #genMask("masks/sub_mask0.png", "mask0", color=[255, 0, 0])
    #im = imread("PAPR_p1.png")
    #subIm = im[1596:1615+1, 1168:1187+1] # ranges not inclusive for max vals
    #print(subIm.shape)
    #plt.imshow(subIm)
    #plt.show()
    #imsave("dot.png", subIm)

    #im = imread("dotted_circle_old.png")
    #im = rescaleIm(im)
    #imsave("dotted_circle_small.png", im)

if __name__ == "__main__":
    main()