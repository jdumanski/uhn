from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PIL import Image
from pdf2image import convert_from_path
import pdf2image
import numpy as np
from matplotlib import pyplot as plt
import copy

# scale factor to get from PNG to PDF coordinates
# png_dim * PNG_TO_PDF = pdf_dim
PNG_TO_PDF = 9/25 

# colors radius around pixel (col, row)
def recolor_radius(image, row, col, color, radius):
    for curr_row in range(row-radius, row+radius+1):
        for curr_col in range(col-radius, col+radius+1):
            image[curr_row, curr_col] = color

def recolor_pixel(image : np.array, _rem_pixel, color=[0, 0, 0], radius=0, bounds=[]):
    #bounds indexing is [[min row, max row], [min col, max col]]
    if bounds == []:
        bounds = [[0, image.shape[0]], [0, image.shape[1]]]

    rem_pixel = copy.deepcopy(_rem_pixel)
    for row in range(bounds[0][0], bounds[0][1]):
        for col in range(bounds[1][0], bounds[1][1]):
            pixel = image[row, col]
            if pixel[0] == rem_pixel[0] and pixel[1] == rem_pixel[1] and pixel[2] == rem_pixel[2]:
                recolor_radius(image, row, col, color, radius)
    
def save_png_from_pdf():
    images = convert_from_path("PAPR_Sample.pdf", poppler_path="C:\\Users\\hocke\\Downloads\\Release-24.07.0-0\\poppler-24.07.0\\Library\\bin")
    image = np.array(images[0])
    prostate_image = image[1030:1864, 480:1622]
    im = Image.fromarray(image)
    im.save("PAPR_p1.png")
    return

#bounds indexing is [[min row, max row], [min col, max col]]
#takes in numpy array, outputs numpy array
#max row and col are NOT inclusive
def get_subimage(image, bounds):
    return image[bounds[0][0] : bounds[0][1], bounds[1][0] : bounds[1][1]]

def open_png():
    pil_im = Image.open("prostate_pic.png")
    prostate_image = np.array(pil_im)
    #print("dot:")
    #dot = prostate_image[595 ,639]
    #print(dot)
    #print("grey background:")
    #grey_back = prostate_image[605, 668]
    #print(grey_back)
    #print("grey background 2:")
    #grey_back_2 = prostate_image[663, 706]
    #print(grey_back_2)
    #dotted_part = prostate_image[509, 897]
    recolor_pixel(prostate_image, [236, 237, 241], color=[255, 255, 255])
    #recolor_pixel(prostate_image, [196, 196, 196], color=[255, 255, 255], radius=3, bounds=[[507, 560],[713, 913]])
    #TODO, pass in list of colors to not recolor (ex navy blue)
    im = Image.fromarray(prostate_image)
    im.show()
    im.save("prostate_pic_mod_ye.png")
    return

#width and height in png coords
#x and y in pdf coords - x and y are bottom right of where png will be placed
def png_to_pdf(canvas: canvas.Canvas, png, width, height, x,y):
    canvas.drawInlineImage(png, x, y, width*PNG_TO_PDF, height*PNG_TO_PDF)

def png_to_pdf_coord(x, y, png_h):
    return x*PNG_TO_PDF, (png_h-1-y)*PNG_TO_PDF

#bounds are [[min row, max row], [min col, max col]]
def save_sub_image(im_path, sub_image_bounds):
    pil_im = Image.open(im_path)
    im = np.array(pil_im)
    sub_im = get_subimage(im, sub_image_bounds)#[[1484, 1530], [889, 936]])
    pil_sub_im = Image.fromarray(sub_im)
    pil_sub_im.show()
    pil_sub_im.save("sub_" + im_path)

#pdf dims: 612x792
#png dims: 1700x2200
#dim ratio: 2.7777 (25/9)
def main():
    #save_png_from_pdf()
    #save_sub_image()
    open_png()

    #below is to export png to pdf
    #c = canvas.Canvas("prostate.pdf", pagesize=letter, bottomup=1)
    #print(letter)
    #pdf_x, pdf_y = png_to_pdf_coord(480, 1864, 2200)
    #png_to_pdf(c, "prostate_pic_mod_white.png", 1142, 834, pdf_x, pdf_y)
    #c.showPage()
    #c.save()
    return

if __name__ == "__main__":
    main()