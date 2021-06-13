from database import Database
class ImagesRepository:
    def __init__(self):
        self.db = Database('localhost','postgres','123456789','5432','multimedia-project')

    def save_image(self, url, mean_color, histogram, color_layout):
        return self.db.update_rows(f"INSERT INTO images_features VALUES (default, '{url}', ARRAY {str(mean_color)}, ARRAY {str(histogram)}, ARRAY {str(color_layout)});")
    def get_all_images(self):
        return self.db.select_rows("SELECT image_url, image_mean_color, image_histogram, image_color_layout FROM images_features;")


# image_repo = ImagesRepository()
# image_repo.save_image("home/images/new_image.png", [1,2,4,5], [1,3,5,6], [1,5,6,7,42])
# print(image_repo.get_all_images())