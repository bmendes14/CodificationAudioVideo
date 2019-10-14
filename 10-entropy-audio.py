import argparse
import itertools
import wave
import os.path
from bitstring import BitString, BitStream

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
# parser.add_argument("output", help="set output file")

args = parser.parse_args()


# noinspection DuplicatedCode
def main():
    # Input validation
    if not args.input:
        print("Input file not set!")
        return

    data = None
    # Open source file
    with wave.open(args.input, 'rb') as file:
        # Read input file params
        nchannels, sampwidth, framerate, nframes, comptype, compname = file.getparams()
        bit_depth = sampwidth / nchannels * 8

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

        data = file.readframes(-1)

    # bit_data = BitStream(bytes=data)
    bit_data = BitStream(bin='001110001101010101011000001100')

    # 1 - Generate possible permutations with defined order
    # Assume finite-context model of order 2
    model_order = 2
    bit_perm = ["".join(seq) for seq in itertools.product("01", repeat=model_order)]

    # Dictionary key is the binary sequence from the permutations set. The dict value is a list of two integers,
    # representing the number of times 0 or 1 was found after the respective binary sequence
    context_dict = dict()

    for bp in bit_perm:
        context_dict[bp] = [0, 0]

    # 00111000
    # Read until the position where a bit_sequence of the desired order fits and the following one
    # So: length - model_order
    while bit_data.pos < bit_data.len-model_order:
        print(str.format('\rPercentage: {:.1f}%', bit_data.pos*1.0/bit_data.len*100.0), end='')
        # Advance one bit in the sequence
        current_bit = bit_data.read('bin:1')
        bit_sequence = current_bit

        # Read model_order next bits. Note that we do not subtract one (one bit is read just before this) from model
        # order because we also want the bit following the bit_sequence
        lookahead_str = bit_data.peek('bin:' + str(model_order))
        bit_sequence += lookahead_str[0:-1]
        bit_value = int(lookahead_str[-1])

        context_dict[bit_sequence][bit_value] = context_dict[bit_sequence][bit_value]+1

    # Pretty print on table
    # new line
    print('')
    for i in range(1, model_order+1):
        print(str.format('n-{}\t', i), end='')

    print(str.format('C(0)\t'), end='')
    print(str.format('C(1)\t'), end='')

    print(str.format('P(0)\t'), end='')
    print(str.format('P(1)\t'), end='')

    for key, value in context_dict.items():

        print (str.format('{}\t{}'))
main()
