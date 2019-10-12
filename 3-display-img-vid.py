from mimetypes import MimeTypes
from urllib import request
import argparse
import wave
import os.path
import cv2 as cv
import numpy as np
import time

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")

args = parser.parse_args()

def main():
	
	if not args.input:
		print ("Input file not set!")
		return
	
	# Determine file type
	mime = MimeTypes()
	url = request.pathname2url(args.input)
	mime_type = mime.guess_type(url)

	# Type could not be determined. Look for extension
	# TODO: refactor if statements
	if mime_type[0] == None:
		ext = args.input.split('.')[1]

		# Video of format YUV4MPEG
		if "y4m" in ext:
			play_video(args.input)

	else:

		type_str = mime_type[0].lower()

		if "image" in type_str:
			show_picture(args.input)

		elif "video" in type_str:
			play_video(args.input)

def play_video(video_file_path):
	cap = cv.VideoCapture(video_file_path)

	# Determine how long we need to wait to comply with defined frame-rate
	frame_interval = int(1000 / cap.get(cv.CAP_PROP_FPS))
	num_of_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)

	# width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)   # float
	# height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT) # float

	frame_counter = 0
	cv.namedWindow('frame', cv.WINDOW_NORMAL)
	while(True):
		try:
			# Capture frame-by-frame
			ret, frame = cap.read()			

			if not ret:
				break

			print (str.format('\rPlaying: {:.1f} // Frame #: {} of {}', frame_counter/num_of_frames, frame_counter, num_of_frames), end='')

			# Our operations on the frame come here
			# gray = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)

			# Display the resulting frame
			cv.imshow('frame', frame)

			cv.waitKey(frame_interval)
			frame_counter += 1

		except Exception as e:
			print(e)

	# When everything done, release the capture
	cv.waitKey(0)
	cap.release()
	cv.destroyAllWindows()

def show_picture(img_file_path):
	cv.imshow('Image', cv.imread(img_file_path, 0))
	cv.waitKey(0)
	cv.destroyAllWindows()


main()