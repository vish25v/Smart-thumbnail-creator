
#from PIL import Image
from PIL import Image, ImageOps
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import os, sys
import cv2
import sys
import math
import numpy as np
import glob
from progressbar import ProgressBar
pbar = ProgressBar()



def resizeImage(infile, output_dir="resized"):
     outfile = os.path.splitext(infile)[0]+""
     extension = os.path.splitext(infile)[1]

     if(infile != outfile and extension == ".svg" and infile!= "croppedpicpp.PNG"):
         drawing = svg2rlg(infile)
         renderPM.drawToFile(drawing,"SVG"+ os.path.splitext(infile)[0] + ".PNG")

#
     if (infile != outfile and infile!= "croppedpicpp.PNG" and extension != ".svg" and "SVG" in os.path.splitext(infile)[0]):
        try :

                size=(300,300)
                im = Image.open(infile)
                imageW,imageH = im.size
                im.thumbnail(size, Image.ANTIALIAS)

                background = Image.new('RGBA', size, (255, 255, 255, 0))
                background2 = Image.new('RGBA', size, (255, 255, 255, 0))

                background.paste(
                   im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2))
                )
                background2.paste(background, (0, 0), background)
                #path = "C:/playground/images/main/resized"
                path = output_dir
                filename = os.path.join(path, outfile)
                background2.save(filename + outfile + ".PNG")



#........................
        except IOError:
            print ("cannot reduce image for ", infile)


if __name__=="__main__":
    output_dir = "resized"
    dir = os.getcwd()

    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)

    for file in pbar(os.listdir(dir)):
        resizeImage(file,output_dir)
