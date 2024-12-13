import argparse

def process_line(line):
    elements = line.split()
    # hacky workaround to not collapse bvals if there are less than 100 elements (likely no replicates)
    # anyway here the combination of triplicates is still hardcoded and would not allow for other replicate numbers
    # TODO this should be properly implemented by taking the bvecs into account
    if len(elements) < 100:
        return line
    processed_elements = []

    current_count = 0
    current_element = None

    for element in elements:
        if element != '0':
            if element == current_element:
                current_count += 1
            else:
                current_element = element
                current_count = 1

            if current_count % 3 == 1:
                processed_elements.append(element)

        else:
            current_element = None
            current_count = 0
            processed_elements.append('0')

    return ' '.join(processed_elements)

def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            processed_line = process_line(line)
            outfile.write(processed_line + '\n')

def main():
    parser = argparse.ArgumentParser(description='Process a text file with consecutive element reduction.')
    parser.add_argument('input_file', help='Input file name')
    parser.add_argument('output_file', help='Output file name')

    args = parser.parse_args()

    process_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()