import os
import json
import cv2
import numpy as np
from argparse import ArgumentParser

# Çıkış klasörünün var olup olmadığını kontrol et, yoksa oluştur
# os.makedirs(output_folder, exist_ok=True)

# JSON dosyasını yükle

class data_prep:

    def __init__(self, image_folder, json_file, output_folder, mode):
        self.image_folder = image_folder  # Sınıfın örnek değişkeni
        self.json_file = json_file  # Sınıfın örnek değişkeni
        self.output_folder = output_folder  # Sınıfın örnek değişkeni
        self.mode = mode  # Sınıfın örnek değişkeni
      
    def process_images(self):

        with open(self.json_file) as f:
            data = json.load(f)

            print(self.json_file)

        for filename in os.listdir(self.image_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):  # Eğer imaj dosyasıysa
                image_path = os.path.join(self.image_folder, filename)
                image = cv2.imread(image_path)

                cv2.imshow("Original Image", image)

                if image is None:
                    print(f"Görüntü yüklenemedi: {image_path}")
                    continue
                
                mask = np.zeros_like(image)
                masked_image = cv2.bitwise_and(image, mask)


                # JSON'dan sürülebilir alan koordinatlarını al
                for frame in data["frames"]:
                    if frame.get("name") and frame["name"].endswith(filename):
                        for label in frame["labels"]:
                            if label.get("category") == self.mode and label.get("poly2d"):
                                    for poly in label["poly2d"]:
                                        
                                        vertices = np.array(poly["vertices"], dtype=np.int32)

                                        print(vertices)

                                        #DRIVABLE İÇİN ÇALIŞACAK
                                        if self.mode == "drivable":                                                   
                                            cv2.fillPoly(masked_image, [vertices],(255, 255, 255))  # Çizgi oluştur ve uygula
            
                                        #LANE İÇİN ÇALIŞACAK                            
                                        elif self.mode == "left_right_lane":
                                            vertices = vertices.reshape((-1, 1, 2))
                                            cv2.polylines(masked_image, [vertices], isClosed=False, color=(255, 255, 255), thickness=2)  # Maske oluştur ve uygula
             
                                                # Çıkış dosya yolunu oluştur
                output_path = os.path.join(self.output_folder, f"{self.mode}_{filename}")

                cv2.imwrite(output_path, masked_image)
                # Sonuçları göstermek için pencereye göster
                cv2.imshow("Masked Image", masked_image)
                # Sonraki görüntüye geçmek için bir tuşa basılmasını bekle
                cv2.waitKey(0)

                cv2.destroyAllWindows()
    

def main():
    parser = ArgumentParser()
    parser.add_argument('--mode', choices=["drivable", "left_right_lane"], default='drivable', help="Mode of operation: 'segment' or 'lane'.")   
    parser.add_argument('--image_folder',type=str, default='../images', help="'.")    
    parser.add_argument('--json_file',type=str, default='../drivable.json', help="'.") 
    parser.add_argument('--output_folder',type=str, default='../drivable', help="'.") 

    args = parser.parse_args()

    if args.mode == 'left_right_lane':
    # Substitute {mode} in json_file and output_folder paths
        args.json_file = '../left_right_lane.json'
        args.output_folder = '../left_right_lane'

    script_dir = os.path.dirname(__file__)
    args.image_folder = os.path.join(script_dir, args.image_folder)
    args.json_file = os.path.join(script_dir, args.json_file)
    args.output_folder = os.path.join(script_dir, args.output_folder)

    os.makedirs(args.output_folder, exist_ok=True)


    DataPrep = data_prep(args.image_folder, args.json_file, args.output_folder, args.mode)

    DataPrep.process_images()

if __name__ == '__main__':
    main()