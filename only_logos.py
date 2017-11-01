
#from PIL import Image
from PIL import Image, ImageOps
import os, sys
import cv2
import sys
import math
import numpy as np
import glob
from progressbar import ProgressBar
pbar = ProgressBar()


def resizeImage(infile, output_dir="resized"):
     outfile = os.path.splitext(infile)[0]+"_resized"
     extension = os.path.splitext(infile)[1]

     if (infile != outfile and infile!= "croppedpicpp.PNG"):
        try :
            #opening image in numpy
            im = Image.open(infile)
            imageW,imageH = im.size
            size=(280,280)
            if imageH <= 100 and imageW <=100:
                im = ImageOps.fit(im, size, method=0, bleed=0.0, centering=(0.5, 0.5))
            else:
                im.thumbnail(size, Image.ANTIALIAS)

            background = Image.new('RGBA', size, (255, 255, 255, 255))
            background2 = Image.new('RGBA', size, (255, 255, 255, 255))

            background.paste(
               im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2))
            )
            background2.paste(background, (0, 0), background)
            img_with_border = ImageOps.expand(background2,border=10,fill='white')
            path = output_dir
            filename = os.path.join(path, outfile)
            img_with_border.save(filename + outfile + ".PNG")

        except IOError:
            print ("cannot reduce image for ", infile)


if __name__=="__main__":
    output_dir = "resized"
    dir = os.getcwd()

    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    for file in pbar(os.listdir(dir)):
        resizeImage(file,output_dir)
