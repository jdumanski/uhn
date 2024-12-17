from pdf2image import convert_from_path
import pdf2image
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def get_shape(file):
    images = convert_from_path(file, poppler_path="C:\\Users\\hocke\\Downloads\\Release-24.07.0-0\\poppler-24.07.0\\Library\\bin")
    image = np.array(images[0])
    print(image.shape)
    return

def main():
    #open_stuff()
    get_shape("prostate.pdf")

if __name__ == '__main__':
    main()