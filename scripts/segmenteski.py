# import os
# import json
# import cv2
# import numpy as np

# # Klasör ve dosya yolları
# image_folder = "/home/damla/catkin_ws/src/data_prep/images"
# json_file = "/home/damla/catkin_ws/src/data_prep/104_eda.json"
# output_folder = "/home/damla/catkin_ws/src/data_prep/segment"

# # Çıkış klasörünün var olup olmadığını kontrol et, yoksa oluştur
# # os.makedirs(output_folder, exist_ok=True)

# # JSON dosyasını yükle
# with open(json_file) as f:
#     data = json.load(f)

# for filename in os.listdir(image_folder):
#     if filename.endswith(".jpg") or filename.endswith(".png"):  # Eğer imaj dosyasıysa
#         image_path = os.path.join(image_folder, filename)
#         image = cv2.imread(image_path)

#         if image is None:
#             print(f"Görüntü yüklenemedi: {image_path}")
#             continue

#         mask = np.zeros_like(image)
#         masked_image = cv2.bitwise_and(image, mask)

#         # JSON'dan sürülebilir alan koordinatlarını al
#         for frame in data["frames"]:
#             if frame.get("name") and frame["name"].endswith(filename):
#                 for label in frame["labels"]:
#                     if label.get("category") == "drivable" and label.get("poly2d"):
#                         for poly in label["poly2d"]:
#                             vertices = np.array(poly["vertices"], dtype=np.int32)
#                             cv2.fillPoly(masked_image, [vertices], (255, 255, 255))  # Maske oluştur ve uygula

#         # Çıkış dosya yolunu oluştur
#         output_path = os.path.join(output_folder, f"segment_{filename}")

#         # Masked image'ı kaydet
#         cv2.imwrite(output_path, masked_image)


#         # Sonuçları göstermek için pencereye göster
#         cv2.imshow("Masked Image", masked_image)
        
#         # Sonraki görüntüye geçmek için bir tuşa basılmasını bekle
#         cv2.waitKey(0)

# cv2.destroyAllWindows()


import os
import json
import cv2
import numpy as np
from argparse import ArgumentParser

class data_prep:

    def __init__(self, image_folder, json_file, output_folder, mode):
        self.image_folder = image_folder
        self.json_file = json_file
        self.output_folder = output_folder
        self.mode = mode
      
    def process_images(self):

        with open(self.json_file) as f:
            data = json.load(f)

        for filename in os.listdir(self.image_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.image_folder, filename)
                image = cv2.imread(image_path)

                if image is None:
                    print(f"Görüntü yüklenemedi: {image_path}")
                    continue
                
                mask = np.zeros_like(image)
                masked_image = image.copy()  # Görüntüyü kopyalayıp üzerinde işlem yapalım

                # JSON'dan sürülebilir alan koordinatlarını al
                for frame in data["frames"]:
                    if frame.get("name") and frame["name"].endswith(filename):
                        for label in frame["labels"]:
                            if label.get("category") == self.mode and label.get("poly2d"):
                                for poly in label["poly2d"]:
                                    vertices = np.array(poly["vertices"], dtype=np.int32)

                                    # DEFAULT VE SEGMENT İÇİN ÇALIŞACAK
                                    if self.mode == "left_right_lane" or self.mode is None:
                                        cv2.fillPoly(mask, [vertices], (255, 255, 255))
                                        masked_image = cv2.bitwise_and(image, mask)
                                        
                                    # LANE YAZARSA ÇALIŞACAK                            
                                    elif self.mode == "drivable":
                                        cv2.polylines(masked_image, [vertices], isClosed=False, color=(255, 255, 255), thickness=2)
                
                output_path = os.path.join(self.output_folder, f"{self.mode}_{filename}")
                cv2.imwrite(output_path, masked_image)
                
                # Sonuçları göstermek için pencereye göster
                cv2.imshow("Masked Image", masked_image)
                # Sonraki görüntüye geçmek için bir tuşa basılmasını bekle
                cv2.waitKey(0)

                cv2.destroyAllWindows()

def main():
    parser = ArgumentParser()
    parser.add_argument('--mode', choices=['drivable', 'left_right_lane'], default='drivable', help="Mode of operation: 'segment' or 'lane'.")
    parser.add_argument('--image_folder', type=str, default='/home/damla/catkin_ws/src/data_prep/images', help="Path to the image folder.")
    parser.add_argument('--json_file', type=str, default='/home/damla/catkin_ws/src/data_prep/drivable.json', help="Path to the JSON file.")
    parser.add_argument('--output_folder', type=str, default='/home/damla/catkin_ws/src/data_prep/drivable', help="Path to the output folder.")

    args = parser.parse_args()

    if args.mode == 'left_right_lane':
        args.json_file = '/home/damla/catkin_ws/src/data_prep/left_right_lane.json'
        args.output_folder = '/home/damla/catkin_ws/src/data_prep/left_right_lane'

    DataPrep = data_prep(args.image_folder, args.json_file, args.output_folder, args.mode)

    DataPrep.process_images()

if __name__ == '__main__':
    main()
