from database import Database
from collections import defaultdict 
class VideoRepository:
    def __init__(self):
        self.db = Database('localhost','postgres','123456789','5432','multimedia-project')

    def save_video(self, url, keyframes):
         self.db.update_rows(f"INSERT INTO videos VALUES (default, '{url}');")
         id = self.db.select_rows(f"SELECT video_id FROM videos WHERE video_url = '{url}';")
         for keyframe in keyframes:
             self.db.update_rows(f"INSERT INTO keyframes VALUES (default, ARRAY {str(keyframe)}, {str(id[0][0])});")

    def get_all_videos(self):
        keyframes =  self.db.select_rows("SELECT videos.video_url, keyframes.keyframes_hist FROM videos, keyframes WHERE videos.video_id = keyframes.video_id;")
        video_dic = defaultdict(list)
        for keyframe in keyframes:
            video_dic[keyframe[0]].append(keyframe[1]) 
        return list(video_dic.items())

# image_repo = VideoRepository()
# image_repo.db.update_rows("DELETE FROM keyframes WHERE video_id = 1;")
# image_repo.db.update_rows("DELETE FROM videos WHERE video_url = 'home/images/new_video.mp4';")
# image_repo.save_video("home/images/new_video2.mp4", [[1,2,4,5,435], [1,3,5,6,456], [1,5,6,7,45]])
# print(image_repo.get_all_videos())