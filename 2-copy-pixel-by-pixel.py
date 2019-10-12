import argparse
import os.path
import cv2 as cv
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("output", help="set output file")

args = parser.parse_args()

def main():
	# Input validation
	if not args.input:
		print ("Input file not set!")
		return

	if not args.output:
		print ("Output file not set!")
		return

	if os.path.isfile(args.output):
		print('Output file exists. Deleting...')
		os.remove(args.output)

	# img = cv.imread(args.input)
	# print (type(img))
	# # 
	# output_img_data = []

	# output_img_data[0][0][0] = "teste"
	# print (output_img_data)

	# for row in range(img.shape[0]):
	# 	output_img_data[row] = []

	# 	for col in range(img.shape[1]):
	# 			output_img_data[row][col] = img[row][col]

	# # px = img[100,100]
	# # print(px)


main()
