import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from video_repository import VideoRepository
from images_repository import ImagesRepository
from CBIR import get_meancolor_value, add_color_layout, compare_color_layout,compare_i_gray_hist, add_histo
from CBVR import *
from flask import Flask
from flask import request
import json
from pathlib import Path
from flask_cors import CORS
# run only once
def save_to_database(videos_path):
    for video in os.listdir(videos_path):
        keyframes=extract_key_frames(os.path.join(videos_path, video))
        for i in range (len(keyframes)):
            keyframes[i]=keyframes[i].flatten().tolist()
        video_repo.save_video(os.path.join(videos_path, video),keyframes)

# application and object setup
app = Flask(__name__)
CORS(app)
video_repo=VideoRepository()
image_repo=ImagesRepository()
downloads_path = str(Path.home() / "Downloads")

# searching api returning similar videos urls
@app.route('/searchvideo/',methods=['POST'])
def upload():
    vid = request.files['video']
    path=''
    if vid:
        path=os.path.join(downloads_path,vid.filename)
        vid.save(path)
        videos_table_data=video_repo.get_all_videos()
        videos=[]

        for video in videos_table_data:
            keyframes=[]
            for keyframe in video[1]:
                keyframes.append(np.array(keyframe).reshape(-1,1).astype(np.float32))
            videos.append(keyframes)
        query_video=extract_key_frames(path)
        alike_videos=get_alike_videos(query_video,videos)

        results=[]
        for i,score in enumerate(alike_videos):
            if score==1:
                
                results.append(videos_table_data[i][0])
        return json.dumps(results)

@app.route('/searchimage/<algr>',methods=['POST'])
def getimage(algr):
    
    path=''
    img=request.files['image']
    if img:
        path=os.path.join(downloads_path,img.filename)
        img.save(path)
        retrieve = image_repo.get_all_images()
        img2 = cv2.imread(path)
        _list = []
        algr=int(algr)
        print(_list)
        if algr == 2:
            for i in range(len(retrieve)):
                if (compare_color_layout(img2, retrieve[i][3]) == 1):
                    print("Appended")
                    _list.append(retrieve[i][0])
        elif algr == 0:
            for b in range(len(retrieve)):
                mean = np.array(retrieve[b][1])
                mean2 = np.array(get_meancolor_value(img2))

                sub = np.abs(np.subtract(mean, mean2))

                if int(sub[0]) < 0.2 * 256 and int(sub[1]) < 0.2 * 256 and int(sub[2]) < 0.2 * 256:
                    _list.append(retrieve[b][0])
        else:
            for b in range(len(retrieve)):
                array = np.array(retrieve[b][2])
                print((compare_i_gray_hist(array.astype(np.float32), img2)))
                if (compare_i_gray_hist(array.astype(np.float32), img2) > 0.6):
                    _list.append(retrieve[b][0])
        print(_list)
        return json.dumps(_list)

if __name__ == '__main__':
    app.run()
    # path = 'D:\\Abdelrhman\\4th computer\\Multimedia\\project\\videos'
    # save_to_database(path)