import sys
import os
import glob
import cv2
import shutil

def convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height):
    ## remove normalization given the size of the image
    x_c = float(x_c_n) * img_width
    y_c = float(y_c_n) * img_height
    width = float(width_n) * img_width
    height = float(height_n) * img_height
    ## compute half width and half height
    half_width = width / 2
    half_height = height / 2
    ## compute left, top, right, bottom
    ## in the official VOC challenge the top-left pixel in the image has coordinates (1;1)
    left = int(x_c - half_width) + 1
    top = int(y_c - half_height) + 1
    right = int(x_c + half_width) + 1
    bottom = int(y_c + half_height) + 1
    return left, top, right, bottom




















with open("class_list.txt") as f:
    obj_list = f.readlines()
    obj_list = [x.strip() for x in obj_list]
  


root_path = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep +os.pardir+os.sep+'yolo3_and_sort/yolov3_detect/testing')
print("[ INFO ] Root:",root_path)
os.chdir(root_path)

if not os.path.exists('true_txt'+os.sep+"map_format"):
    os.makedirs('true_txt'+os.sep+"map_format")
else:
 
    shutil.rmtree('true_txt'+os.sep+'map_format')
    os.makedirs('true_txt'+os.sep+"map_format")




true_txt = [os.path.basename(x) for x in glob.glob('true_txt/yolo_format/*.txt')]
true_txt.remove('classes.txt')
assert len(true_txt) != 0

## 1. CHECKING
for tmp_file in true_txt:

    ann_txt = tmp_file.split('.txt')[0]
    print('ann_txt : ',ann_txt)

    print("[ INFO ] Finding images in",root_path)
    images =glob.glob('*.jpg') 

    for fname in images:
        if fname.startswith(ann_txt):

            img = cv2.imread(fname)

            img_height, img_width = img.shape[:2]
            print(fname)
            break
        #else:    
            #print("Not found",fname)
      
    ## 2. CONVERT
    with open('true_txt'+os.sep+'yolo_format'+os.sep+tmp_file) as f:
 
        content = f.readlines()   
        content = [x.strip() for x in content]      
     

        with open('true_txt'+os.sep+'map_format'+os.sep+tmp_file, "a") as new_f:#make new txt
            for line in content:               
                obj_id, x_c_n, y_c_n, width_n, height_n = line.split()
                obj_name = obj_list[int(obj_id)]
                left, top, right, bottom = convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height)

                new_f.write(obj_name + " " + str(left) + " " + str(top) + " " + str(right) + " " + str(bottom) + '\n')

