import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys



def copy_img(read_image, write_image):
    img = cv2.imread(read_image)
    pixel= img[200, 550]
    rows,cols = img.shape[0],img.shape[1]
    print(rows)
    blank_image = np.zeros((rows,cols,3), np.uint8)
    cv2.imshow("blanck",blank_image)
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            blank_image[i,j] = img[i, j]
    cv2.imshow("copied image",blank_image)
    cv2.imwrite(write_image,blank_image)
    cv2.waitKey(0)


copy_img(sys.argv[1],sys.argv[2])