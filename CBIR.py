# importing required libraries of opencv
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from images_repository import ImagesRepository
def get_meancolor_value(myimg):
    avg_color_per_row = np.average(myimg, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color.tolist()
def add_histo(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]) / 255

    return hist.flatten().tolist()


def compare_i_gray_hist(hist,image2):
    hist=np.array([[i] for i in hist])
    image2=cv2.cvtColor(image2, cv2.COLOR_RGB2HSV)
    hist2= cv2.calcHist([image2], [0], None, [256], [0, 256])/255
    return cv2.compareHist(hist2,hist,cv2.HISTCMP_CORREL)
def add_color_layout(image):
    colorlayout=[]

    image = cv2.resize(image, (1152, 960), interpolation=cv2.INTER_AREA)
    for r in range (15):

        for b in range(18):
            mean = np.zeros((1, 3))
            for i in range(3):
                mean[0, i] = np.mean(image[64*r:64*(r+1), 64*b:64*(b+1), i])/255
            colorlayout.append(mean)
    colorlayout=np.array(colorlayout).reshape(-1)
    return colorlayout.tolist()

    
def compare_color_layout(image1,color):
    color=np.array(color).reshape(270,3)
    score=0
    image1=cv2.resize(image1,(1152,960),interpolation = cv2.INTER_AREA)
    index=0


    for r in range (15):

        for b in range(18):
            mean = np.zeros((1, 3))
            for i in range(3):
                mean[0, i] = np.mean(image1[64*r:64*(r+1), 64*b:64*(b+1), i])/255

            sub=np.abs(np.subtract(mean,color[index])).reshape(-1)
            index+=1
            if  sub[0]<0.4 and sub[1]<0.4 and sub[2]<0.4:

                score+=1


    print("The sore is :",(score/270)*100,"%")
    if (score/270)*100 >=55 :
        #print(score)
        return 1
    else:
        return 0

image_repo=ImagesRepository()


# plt.show()


# image_repo=ImagesRepository()
# #####################################processing data ##############################################
# path="D:\\Abdelrhman\\4th computer\\Multimedia\\project\\images"
# files_and_directories = os.listdir(path)
# for item in files_and_directories :
#     path_ = path+'/'+item
#     img1=cv2.imread(path_)
#     image_repo.save_image(path_,get_meancolor_value(img1),add_histo(img1),add_color_layout(img1) )