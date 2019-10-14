import argparse
import itertools
import wave
import os.path
from bitstring import BitString, BitStream
from prettytable import PrettyTable

parser = argparse.ArgumentParser()

parser.add_argument("input", help="set input file")
parser.add_argument("--order", help="set the finite-context model order", required=True)
args = parser.parse_args()


# noinspection DuplicatedCode
def main():
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

    bit_data = BitStream(bytes=data)
    # bit_data = BitStream(bin='001110001101010101011000001100')

    # 1 - Generate possible permutations with defined order
    # Assume finite-context model of order 2
    model_order = int(args.order)
    bit_perm = ["".join(seq) for seq in itertools.product("01", repeat=model_order)]

    # Dictionary key is the binary sequence from the permutations set. The dict value is a list of two integers,
    # representing the number of times 0 or 1 was found after the respective binary sequence
    context_dict = dict()

    for bp in bit_perm:
        context_dict[bp] = [0, 0]

    # 00111000
    # Read until the position where a bit_sequence of the desired order fits and the following one
    # So: length - model_order
    while bit_data.pos < bit_data.len - model_order:
        print(str.format('\rPercentage: {:.1f}%', bit_data.pos * 1.0 / bit_data.len * 100.0), end='')
        # Advance one bit in the sequence
        current_bit = bit_data.read('bin:1')
        bit_sequence = current_bit

        # Read model_order next bits. Note that we do not subtract one (one bit is read just before this) from model
        # order because we also want the bit following the bit_sequence
        lookahead_str = bit_data.peek('bin:' + str(model_order))
        bit_sequence += lookahead_str[0:-1]
        bit_value = int(lookahead_str[-1])

        context_dict[bit_sequence][bit_value] = context_dict[bit_sequence][bit_value] + 1

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

main()
