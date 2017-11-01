
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
            #declaring CascadeClassifier:
            cascPath = "haarcascade_frontalface_alt2.xml"
            # Create the haar cascade
            faceCascade = cv2.CascadeClassifier(cascPath)
            #opening image in cv2
            imagePath = infile
            imageCV = cv2.imread(imagePath)
            #finding if there is a face in the image
            #converting image to gray image to detect faces
            gray = cv2.cvtColor(imageCV, cv2.COLOR_BGR2GRAY)
            side = math.sqrt(imageCV.size)
            minlen = int(side / 20)
            maxlen = int(side / 2)
            foundFace = ""
            faces = faceCascade.detectMultiScale(gray,1.3, 4, 0, (minlen, minlen), (maxlen, maxlen))
            #print ("Found {0} faces!".format(len(faces)))
            #checking how many faces found:
            #if 0, do regular crop, if more than one found, change parameters to get only one faceCascade
            #if one face found, call def foundFace to crop w.r.t to face
            #if (len(faces)) == 1 :
            #    foundFace = "yes"
            #elif (len(faces)) > 1 :
            #    foundFace = "moreFaces"
            #    faces = faceCascade.detectMultiScale(gray,1.4, 5, 0, (minlen, minlen), (maxlen, maxlen))
            #elif (len(faces)) == 0 :
            #    foundFace = "no"
                #do regular cropping since no face was found
            #........
            def detectface(imagefile):
                imagefile = imageCV
                for (x, y, w, h) in faces:
                          #these parametersare for original pic to get ration of sides Left around the face.
                          #cv2.rectangle(imageCV, (x, y), (x+w, y+h), (0, 255, 0), 2)
                          #print((x,y),(x+w, y),(x+w, y+h), (x, y+h))
                          #cv2.imshow("face Image", imageCV)
                          Lw = x
                          Rw = imageW-(x+w)
                          Th = y
                          Bh = imageH-(y+h)
                          ThRatio = Th/(Th+Bh)
                          BhRatio = Bh/(Th+Bh)
                          LwRatio = Lw/(Lw+Rw)
                          RwRatio = Rw/(Lw+Rw)
                          nTh, nBh, nRw, nLw = 0, 0, 0, 0

                          if(imageH<imageW):
                              nTh = ThRatio * (imageH - h)
                              nBh = BhRatio * (imageH - h)
                              nRw = RwRatio * (imageH - w)
                              nLw = LwRatio * (imageH - w)
                          else:
                              nTh = ThRatio * (imageW - h)
                              nBh = BhRatio * (imageW - h)
                              nRw = RwRatio * (imageW - w)
                              nLw = LwRatio * (imageW - w)

                          nTh = int(round(nTh))
                          nBh = int(round(nBh))
                          nLw = int(round(nLw))
                          nRw = int(round(nRw))
                          roi = imageCV[ y - nTh : y + h + nBh , x - nLw :  x + w + nRw ]
                          cv2.imwrite( "croppedpicpp.PNG", roi );

                          #cv2.imshow("Cropped Imagepp", roi)
                          #cv2.waitKey(0)
                          im2 = Image.open("croppedpicpp.PNG")
                          im2 = ImageOps.fit(im2, (300,300), method=0, bleed=0.0, centering=(0.5, 0.5))
                          #im2.save("finalcrop"+ imagePath +"finalpp.PNG")
                          #path = "C:/playground/images/main/resized"
                          path = output_dir
                          filename = os.path.join(path, outfile)
                          im2.save(filename +" FACE_DETECTED" +  ".PNG")


  #............................End of def detectface().............................


            if (len(faces)) == 0:
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
                #path = "C:/playground/images/main/resized"
                path = output_dir
                filename = os.path.join(path, outfile)
                img_with_border.save(filename + outfile + ".PNG")

            elif (len(faces)) == 1:
                detectface(imageCV)

            elif (len(faces)) > 1:
                # increase the parameter value, scalescaleFactor=1.4,minNeighbors=5,
                faces = faceCascade.detectMultiScale(gray,1.4, 5, 0, (minlen, minlen), (maxlen, maxlen))
                detectface(imageCV)







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
