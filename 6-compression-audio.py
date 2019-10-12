import argparse
import wave
import os.path
from bitstring import BitStream

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("output", help="set output file")

args = parser.parse_args()

def quantitize_bit_sequence(data):
	bit_sequence = ''
	for i, byte in zip(range(0, len(data)), data):
		print(str.format('\rProcessing... {:.2f}', i/len(data) * 100), end='')

		nb = byte >> 2
		bin_repr = bin(nb)[2:]

		if len(bin_repr) < 6:
			for j in range(0, 6-len(bin_repr)):
				bin_repr = '0' + bin_repr

		elif len(bin_repr) > 6:
			bin_repr = bin_repr[0:-2]

		bit_sequence += bin_repr
		# print("Byte:\t\t", byte, "\tBin: \t", bin(byte)[2:])
		# print("Shifted:\t", nb, "\tBin: \t", bin(nb)[2:])
		# print("Bin: \t", bin_repr)

		# string = string + bin(byte)[2:-2]
		# print ("Number: ", bin(nb))
		# print ("Number: ", bin(nb))
		# print('\n', string)
		# return

	print(bit_sequence[0:10])

	bytes = int(bit_sequence, 2).to_bytes(len(bit_sequence) // 8, byteorder='big')
	print(len(bytes))

def main():
	# Input validation
	if not args.input:
		print("Input file not set!")
		return

	if not args.output:
		print("Output file not set!")
		return

	if os.path.isfile(args.output):
		print('Output file exists. Deleting...')
		os.remove(args.output)

	# Open source file
	with wave.open(args.input, 'rb') as file:
		# Read input file params
		nchannels, sampwidth, framerate, nframes, comptype, compname = file.getparams()
		bit_depth = sampwidth/nchannels*8

		if bit_depth % 8 != 0:
			print('Bit depth is not a multiple of 8. Ma come?!')
			return

		bit_depth = int(bit_depth)
		print("Input file:\t", args.input)
		print("No Channels:\t", nchannels)
		print("Sample Width:\t", sampwidth)
		print("Framerate:\t", framerate)
		print("No frames:\t", nframes)
		print("Comp Type:\t", comptype)
		print("Comp Name:\t", compname)
		print("Bit-depth:\t", bit_depth)

		# Open target file with same params (conversion of channel or similar would be here)
		output_file = wave.open(args.output, 'wb')
		output_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

		new_file = ''
		# with open(args.input, "rb") as f:
		# 	fsize = os.fstat(f.fileno()).st_size
		# 	byte = f.read(1)

		string = ''
		data = file.readframes(-1)

		# Method 1
		quantitize_bit_sequence(data)

		return
		# b = BitStream(bytes=byte)

		# while bit_stream.bitpos <
		# Took: 2.19min with read and manual bit_stream.pos + 8
		# while bit_stream.pos < bit_stream.length:
			# print(str.format('\rProcessing... {:.2f}', bit_stream.pos / bit_stream.length * 100), end='')
			# Sample in binary
			# sample_bin = bit_stream.read(bit_depth)
			# bit_stream.pos = bit_stream.pos + 8
			# new.append(sample_bin)

		# Took 40s to read byte by byte
		# counter = 1


		# with open(args.output, 'wb') as output_file:
		# 	new.tofile(output_file)

main()