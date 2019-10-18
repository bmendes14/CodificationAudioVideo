import argparse
import itertools
import os.path
from bitstring import BitString, BitStream
from prettytable import PrettyTable
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from mimetypes import MimeTypes
from urllib.parse import urlparse
from urllib.request import pathname2url
import math


parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("--order", help="set the finite-context model order", required=True)
args = parser.parse_args()


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
            videoInput(request)

    else:

        type_str = mime_type[0].lower()

        if "image" in type_str:
            imageInput(request)

        elif "video" in type_str:
            videoInput(request)

def videoInput(files):
    data = None
    # Open source file
    cap = cv2.VideoCapture(files)
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    val = dict()
    frame_count = 0
    while(cap.isOpened()):    
        # Capture frame-by-frame 
        ret, frame = cap.read() 
        if ret == True:   
            print(str.format('\rPercentage: {:.1f}%', frame_count * 1.0 / length * 100.0), end='')
            data = frame[:,:,0]
            
            for i in range(0,256):
                val[(i)] = [0]*256

            for x in range(0,data.shape[0]):
                for y in range(0,data.shape[1]):
                    if x-1 > 0:
                        curr_pixel_value = data[x,y]
                        prev_pixel_value = data[x-1,y]
                        val[(prev_pixel_value)][curr_pixel_value] =val[(prev_pixel_value)][curr_pixel_value] + 1
        else:
            print(cap.read()[0])  
            break
        frame_count = frame_count +1

    cap.release() 
    calculateEntropy(val)

def imageInput(files):
    
    # Open source file
    data = cv2.imread(files)
    data = data[:,:,0]
    val = dict()
    for i in range(0,256):
        val[(i)] = [0]*256

    for x in range(0,data.shape[0]):
        for y in range(0,data.shape[1]):
            if x-1 > 0:
                curr_pixel_value = data[x,y]
                prev_pixel_value = data[x-1,y]
                val[(prev_pixel_value)][curr_pixel_value] =val[(prev_pixel_value)][curr_pixel_value] + 1 
    calculateEntropy(val)
    

    

# noinspection DuplicatedCode
def calculateEntropy(val):
    

    Htropia = [0]*256
    count = 0
    for k,v in val.items():
        p = [0]*256
        total = sum(v)
        for i in range(0,len(v)):
            p[i] = p[i] + v[i]/total
        H=0
        for i in range(0,len(p)):
            if(p[i]>0.0):
                H = H + p[i] * math.log2(p[i])
        Htropia[k] = -1 * H
        count = count +1
    x = [i for i in range(0,len(Htropia))]
    y = [Htropia[i] for i in range(0,len(Htropia))]
    plt.plot(x, y)
    plt.show()



main(sys.argv[1])
