import argparse
from helper_functions import get_similar_vectors

def read_file_to_list_of_lists(input_filename):
    with open(input_filename, 'r') as infile:
        return [line.split() for line in infile.readlines()]

def write_list_of_lists_to_file(output_filename, list_of_lists):
    with open(output_filename, 'w') as outfile:
        for line in list_of_lists:
            outfile.write(' '.join(line) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Process related bval and bvec files with consecutive element reduction.')
    parser.add_argument('bval_in', help='Input bval file name')
    parser.add_argument('bvec_in', help='Input bvec file name')
    parser.add_argument('bval_out', help='Output bval file name')
    parser.add_argument('bvec_out', help='Output bvec file name')

    args = parser.parse_args()

    bval_lines = read_file_to_list_of_lists(args.bval_in)
    bvec_lines = read_file_to_list_of_lists(args.bvec_in)
    zero_indices, replicate_indices = get_similar_vectors(bvec_lines)
    indices_to_keep = sorted(zero_indices + [sublist[0] for sublist in replicate_indices])

    bval_lines = [[line[i] for i in indices_to_keep] for line in bval_lines]
    bvec_lines = [[line[i] for i in indices_to_keep] for line in bvec_lines]

    write_list_of_lists_to_file(args.bval_out, bval_lines)
    write_list_of_lists_to_file(args.bvec_out, bvec_lines)

if __name__ == "__main__":
    main()