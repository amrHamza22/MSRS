import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
#import video_repository
def visualize_hist(image):
    hist_R = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_G = cv2.calcHist([image], [1], None, [256], [0, 256])
    hist_B = cv2.calcHist([image], [2], None, [256], [0, 256])
    plt.plot(hist_R,label='red',color='r')
    plt.plot(hist_G,label='green',color='g')
    plt.plot(hist_B,label='blue',color='b')
    plt.legend()
    plt.show()
def compare_gray_hist(image1,image2):
    return cv2.compareHist(image1,image2,cv2.HISTCMP_CORREL)
def naive_score(vid1,vid2):
    count=0
    for key_frame in vid1:
        for frame_to_be_searched in vid2:
            if compare_gray_hist(key_frame, frame_to_be_searched) >= 0.70:
                count=count+1
                break

    print("vid: " + str(len(vid1)))
    return count/len(vid1)
def get_alike_videos(video,videos):
    alike=[0]*len(videos)
    for i,candidate in enumerate(videos):
        print(naive_score(video,candidate))
        if naive_score(video,candidate)>0.35:
            alike[i]=1
        else:
            alike[i]=0
    return alike
def extract_key_frames(video):
    vidcap = cv2.VideoCapture(video)
    vidcap.set(3, 1280)
    vidcap.set(4, 720)
    success, image = vidcap.read()
    key_frames = []
    key_frames.append(cv2.calcHist([image], [0], None, [256], [0, 256]))
    while success:
        success, image2 = vidcap.read()
        try:
            if compare_gray_hist(cv2.calcHist([image], [0], None, [256], [0, 256]), cv2.calcHist([image2], [0], None, [256], [0, 256])) <= 0.4:
                image = image2
                key_frames.append(cv2.calcHist([image], [0], None, [256], [0, 256]))
                # print('new key frame')
        except cv2.error as e:
            print('invalid frame')
    return key_frames
#### testing
# vid_1_key_frames=extract_key_frames('videoplayback.mp4')
# print(vid_1_key_frames)
# vid_2_key_frames=extract_key_frames('videoplayback.mp4')
# print(naive_score(vid_1_key_frames,vid_2_key_frames))