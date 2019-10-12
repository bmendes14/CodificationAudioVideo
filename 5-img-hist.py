import matplotlib.pyplot as plt
from mimetypes import MimeTypes
from urllib import request
import argparse
import cv2 as cv

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")

args = parser.parse_args()

def main():
	# Input validation
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
			calc_hist_video(args.input)

	else:

		type_str = mime_type[0].lower()

		if "image" in type_str:
			calc_hist_img(args.input)

		elif "video" in type_str:
			calc_hist_video(args.input)

	
def calc_hist_img(img_file_path):
	img = cv.imread(args.input)
	color = ('b','g','r')

	plt.figure(0)

	for i, col in enumerate(color):
		histr = cv.calcHist([img],[i],None,[256],[0,256])
		plt.plot(histr, color = col)
		plt.xlim([0,256])

	plt.figure(1)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	plt.hist(gray.ravel(),256,[0,256])
	plt.show()

def calc_hist_video(video_file_path):
	cap = cv.VideoCapture(video_file_path)

	# Determine how long we need to wait to comply with defined frame-rate
	frame_interval = int(1000 / cap.get(cv.CAP_PROP_FPS))
	num_of_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)

	frames = []
	gray_frames = []

	while(True):
		try:
			# Capture frame-by-frame
			ret, frame = cap.read()			

			if not ret:
				break

			frames.append(frame)
			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			gray_frames.append(gray)

		except Exception as e:
			print(e)

	color = ('b','g','r')

	plt.figure(0)

	for i, col in enumerate(color):
		histr = cv.calcHist(frames,[i],None,[256],[0,256])
		plt.plot(histr, color = col)
		plt.xlim([0,256])

	plt.figure(1)
	g_histr = cv.calcHist(gray_frames, [0], None, [256], [0,256])
	plt.plot(g_histr)
	plt.show()

main()