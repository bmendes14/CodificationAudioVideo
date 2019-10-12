                # Took: 2.19min with read and manual bit_stream.pos + 8
                while bit_stream.pos < bit_stream.length:
                    print(str.format('\rProcessing... {:.2f}', bit_stream.pos / bit_stream.length * 100), end='')
                    # Sample in binary
                    sample_bin = bit_stream.read(bit_depth)
                    bit_stream.pos = bit_stream.pos + 8
                    # new.append(sample_bin)


                # 4:30.51
                while bit_stream.pos < bit_stream.length:
                    print(str.format('\rProcessing... {:.2f}', bit_stream.pos / bit_stream.length * 100), end='')
                    # Sample in binary
                    sample_bin = bit_stream.read(bit_depth)
                    # new.append(sample_bin)


        # Took 40s to read byte by byte
		# counter = 1
		with open(args.input, "rb") as f:
			fsize = os.fstat(f.fileno()).st_size
			byte = f.read(1)
			while byte:
				# print(str.format('\rProcessing... {:.2f}', bit_stream.pos / bit_stream.length * 100), end='')
				print(str.format('\rProcessing... {:.2f}', f.tell()/fsize*100), end='')
				# Do stuff with byte
				byte = f.read(1)
