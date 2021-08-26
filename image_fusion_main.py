from PIL import Image,ImageChops
from PIL import ImageFilter
import cv2
import math
import numpy as np
import skimage.measure

#SAVING IMAGES IN OBJECTS
infra=Image.open('infra.jpg')
optic=Image.open('optic.jpg')
#infra,optic-ORIGINAL IMAGES

#RESIZING IMAGES AND SAVING THEM
infra1=infra.resize((500,350))
optic1=optic.resize((500,350))
infra1.save('infra1.jpg')
optic1.save('optic1.jpg')
#infra1,optic1-RESIZED IMAGES

#APPLYING MEDIAN FILTER
optic2 = optic1.filter(ImageFilter.MedianFilter(size = 3))  
infra2 = infra1.filter(ImageFilter.MedianFilter(size = 3))
infra2.save('infra2.jpg')
optic2.save('optic2.jpg')
#infra2,optic2-FILTERED IMAGES

#FUSION 1-ADD USING OPENCV
infra3=cv2.imread('infra2.jpg')
optic3=cv2.imread('optic2.jpg')
fusion1=cv2.add(infra3,optic3)
cv2.imwrite('fusion1.jpg',fusion1)
#cv2.imshow('fusion1',fusion1)

#FUSION2-ADDWEIGHT with OPENCV
fusion2=cv2.addWeighted(infra3,0.8,optic3,0.2,0)
cv2.imwrite('fusion2.jpg',fusion2)
#cv2.imshow('fusion2',fusion2)

#FUSION3-ADDWEIGHT with OPENCV,gamma=2
fusion3=cv2.addWeighted(infra3,0.8,optic3,0.2,2)
cv2.imwrite('fusion3.jpg',fusion3)
#cv2.imshow('fusion3',fusion3)

#FUSION4-BLENDING IMAGES
fusion4 = Image.blend(infra2, optic2, 0.0)
fusion4.save('fusion4.jpg')
#fusion4.show()

#ROOT MEAN SQUARE ERROR
print("**********************************************************************************")
print("On Basis On ROOT MEAN SQUARE ERROR(RMSE) Between Two Images")
print("**********************************************************************************")
fusion5=Image.open('fusion1.jpg')
fusion6=Image.open('fusion2.jpg')
fusion7=Image.open('fusion3.jpg')
def rmsdiff(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    errors = np.asarray(ImageChops.difference(im1, im2)) / 255
    return math.sqrt(np.mean(np.square(errors)))
error=[]
error1=rmsdiff(infra2,fusion5)
error2=rmsdiff(infra2,fusion6)
error3=rmsdiff(infra2,fusion7)
error4=rmsdiff(infra2,fusion4)
print("Root mean square error of fusion1: ",error1,"\nRoot mean square error of fusion2: ",error2,"\nRoot mean square error of fusion3: ",error3,"\nRoot mean square error of fusion4: ",error4)
error.append(error1)
error.append(error2)
error.append(error3)
error.append(error4)
num1=min(error)
for i in range(0,4):
    if num1==error[i]:
        print("On basis of ROOT MEAN SQUARE ERROR(RMSE),the fusion ",i+1,"is Better!")
        break

#PEAK SIGNAL-TO-NOISE RATIO
print("\n**********************************************************************************")
print("On Basis On PEAK SIGNAL-TO-NOISE RATIO Between Two Images")
print("**********************************************************************************")
infra10=cv2.imread('infra2.jpg')
fusion8=cv2.imread('fusion4.jpg')
def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
          return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
d=[]
d1=psnr(infra10,fusion1)
d2=psnr(infra10,fusion2)
d3=psnr(infra10,fusion3)
d4=psnr(infra10,fusion8)
print("Peak signal-to-noise ratio of fusion1: ",d1,"\nPeak signal-to-noise ratio of fusion2: ",d2,"\nPeak signal-to-noise ratio of fusion3: ",d3,"\nPeak signal-to-noise ratio of fusion4: ",d4)
d.append(d1)
d.append(d2)
d.append(d3)
d.append(d4)
num2=min(d)
for i in range(0,4):
    if num2==d[i]:
        print("On basis of PEAK SIGNAL-TO-NOISE RATIO,the fusion ",i+1,"is Better!")
        break

 #ENTROPY OF IMAGES
print("\n**********************************************************************************")
print("On Basis On ENTROPY OF IMAGES")
print("**********************************************************************************")
entropy=[]
entropy1 = skimage.measure.shannon_entropy(fusion1)
entropy2 = skimage.measure.shannon_entropy(fusion2)
entropy3 = skimage.measure.shannon_entropy(fusion3)
entropy4 = skimage.measure.shannon_entropy(fusion4)
print("\nEntropy of fusion1: ",entropy1,"\nEntropy of fusion2: ",entropy2,"\nEntropy of fusion3: ",entropy3,"\nEntropy of fusion4: ",entropy4)
entropy.append(entropy1)
entropy.append(entropy2)
entropy.append(entropy3)
entropy.append(entropy4)
num3=min(entropy)
for i in range(0,4):
    if num3==entropy[i]:
        print("On basis of ENTROPY OF IMAGES,the fusion ",i+1,"is Better!")
        break
