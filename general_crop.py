
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
            size=(300,300)
            im = ImageOps.fit(im, size, method=0, bleed=0.0, centering=(0.5, 0.5))

            path = output_dir
            filename = os.path.join(path, outfile)
            im.save(filename + outfile + ".PNG")

        except IOError:
            print ("cannot reduce image for ", infile)


if __name__=="__main__":
    output_dir = "resized"
    dir = os.getcwd()

    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    for file in pbar(os.listdir(dir)):
        resizeImage(file,output_dir)
