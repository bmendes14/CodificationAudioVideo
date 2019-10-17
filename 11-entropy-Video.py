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
    model_order = int(args.order)
    bit_perm = ["".join(seq) for seq in itertools.product("01", repeat=model_order)]
    
    context_dict = dict()

    for bp in bit_perm:
        context_dict[bp] = [0, 0]

    frame_count = 0
    while(cap.isOpened()):    
        # Capture frame-by-frame 
        ret, frame = cap.read() 
        if ret == True:   
            print(str.format('\rPercentage: {:.1f}%', frame_count * 1.0 / length * 100.0), end='\n')
            context_dict  = calculateEntropy(frame,context_dict,model_order)
            frame_count = frame_count + 1
        else:
            print(cap.read()[0])  
            break

    cap.release() 

    # Get all information from all frames
    #data = cap.read()[1]
    #model_order,context_dict = calculateEntropy(data)
    drawResults(model_order,context_dict)

def imageInput(files):
    data = None
    model_order = int(args.order)
    bit_perm = ["".join(seq) for seq in itertools.product("01", repeat=model_order)]
    
    context_dict = dict()

    for bp in bit_perm:
        context_dict[bp] = [0, 0]

    # Open source file
    data = cv2.imread(files)
    context_dict  = calculateEntropy(data,context_dict,model_order)
    drawResults(model_order,context_dict)


# noinspection DuplicatedCode
def calculateEntropy(data, context_dict,model_order):

    bit_data = BitStream(bytes=data)
    #print(bit_data)
    # bit_data = BitStream(bin='001110001101010101011000001100')

    # 1 - Generate possible permutations with defined order
    # Assume finite-context model of order 2
    # model_order = int(args.order)
    # bit_perm = ["".join(seq) for seq in itertools.product("01", repeat=model_order)]

    # Dictionary key is the binary sequence from the permutations set. The dict value is a list of two integers,
    # representing the number of times 0 or 1 was found after the respective binary sequence
    # context_dict = dict()

    # for bp in bit_perm:
    #     context_dict[bp] = [0, 0]

    # 00111000
    # Read until the position where a bit_sequence of the desired order fits and the following one
    # So: length - model_order
    while bit_data.pos < bit_data.len - model_order:
        print(str.format('\rPercentage2: {:.1f}%', bit_data.pos * 1.0 / bit_data.len * 100.0), end='')
        # Advance one bit in the sequence
        current_bit = bit_data.read('bin:1')
        bit_sequence = current_bit

        # Read model_order next bits. Note that we do not subtract one (one bit is read just before this) from model
        # order because we also want the bit following the bit_sequence
        lookahead_str = bit_data.peek('bin:' + str(model_order))
        bit_sequence += lookahead_str[0:-1]
        bit_value = int(lookahead_str[-1])

        context_dict[bit_sequence][bit_value] = context_dict[bit_sequence][bit_value] + 1

    return context_dict


def drawResults(model_order,context_dict):
    print("\nResults:")

    x = PrettyTable()

    x.field_names = [str.format('FCM {}-bit seq', model_order),
                     'C(0)',
                     'C(1)',
                     'P(0)',
                     'P(1)']

    for key, value in context_dict.items():
        total = value[0] + value[1]
        x.add_row([key,
                  value[0],
                  value[1],
                  round(value[0] / total * 100, 2),
                  round(value[1] / total * 100, 2)])

    print(x)

main(sys.argv[1])
