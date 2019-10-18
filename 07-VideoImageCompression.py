import wave
import struct
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import statistics
from math import floor
from mimetypes import MimeTypes
from urllib.parse import urlparse
from urllib.request import pathname2url

def compressionImage(read_image, write_image, compression_num):
    img = cv2.imread(read_image)
    rows,cols = img.shape[0],img.shape[1]
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    reduzida = np.zeros((rows,cols,3))
    revertida = np.zeros((rows,cols,3))

    reduzida = ((pow(2,int(compression_num))-1)/255) * (img)
    # for i in range(1,img.shape[0]-1):
    #     for j in range(1,img.shape[1]-1):
    #         reduzida[i,j] = ((pow(2,int(compression_num))-1)/255) * (img[i, j])
    

    reduzida = reduzida.astype(np.uint8)
    revertida = ((255/(pow(2,int(compression_num))-1))) * (reduzida)
    # for i in range(1,reduzida.shape[0]-1):
    #     for j in range(1,reduzida.shape[1]-1):
    #         revertida[i,j] = ((255/(pow(2,int(compression_num))-1))) * (reduzida[i, j])
            

    revertida = revertida.astype(np.uint8)
    print(img[10,10])
    print(reduzida[10,10])
    print(revertida[10,10])
    cv2.imshow("Original",img)
    cv2.imshow("reduzida",reduzida)
    cv2.imshow("revertida",revertida)
    cv2.waitKey(0)
    cv2.imwrite('revertida_'+write_image,revertida)
    cv2.imwrite('reduzida_'+write_image,reduzida)
    print(type(img[10,10][0]))
    print(type(revertida[10,10][0]))
    print(type(reduzida[10,10][0]))



def compressionVideo(read_image, write_image, compression_num):
    cap = cv2.VideoCapture(read_image)
    # print(cap.read()[0])  
    if(cap.read()[0] != False):
        if(cap.isOpened() == False):
            print("Error opening video  file")
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeigth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frameSize = frameHeigth * frameWidth
        # fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fourcc = cv2.VideoWriter_fourcc(*'X264')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        videoWriter= cv2.VideoWriter(write_image,fourcc,fps,(frameHeigth,frameWidth))
        while(cap.isOpened()):    
            # Capture frame-by-frame 
            ret, frame = cap.read() 
            if ret == True:     
                reduzida = np.zeros((frameWidth,frameHeigth,3))
                revertida = np.zeros((frameWidth,frameHeigth,3))
                reduzida = ((pow(2,int(compression_num))-1)/255) * (frame)
                reduzida = reduzida.astype(np.uint8)
                revertida = ((255/(pow(2,int(compression_num))-1))) * (reduzida)  
                revertida = revertida.astype(np.uint8)  
                # Display the resulting frame 
                cv2.imshow('Frame Original', frame) 
                cv2.imshow('Frame Revertido', revertida) 

                videoWriter.write(revertida)
            
                # Press Q on keyboard to  exit 
                if cv2.waitKey(25) & 0xFF == ord('q'): 
                    break
            # Break the loop 
            else:
                print(cap.read()[0])  
                break
        cap.release()
            

def main(request):
    # Determine file type
    mime = MimeTypes()
    # url = request.pathname2url(args.input)
    mime_type = mime.guess_type(request)

    # Type could not be determined. Look for extension
    # TODO: refactor if statements
    if mime_type[0] == None:
        ext = request.split('.')[1]

        # Video of format YUV4MPEG
        if "y4m" in ext:
            compressionVideo(sys.argv[1],sys.argv[2],sys.argv[3])

    else:

        type_str = mime_type[0].lower()

        if "image" in type_str:
            compressionImage(sys.argv[1],sys.argv[2],sys.argv[3])

        elif "video" in type_str:
            compressionVideo(sys.argv[1],sys.argv[2],sys.argv[3])

main(sys.argv[1])





