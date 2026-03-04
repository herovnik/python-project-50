import argparse
import json


def main():
    parser = argparse.ArgumentParser(
                        prog='gendiff',
                        description='Compares two configuration files and shows a difference')

    parser.add_argument('-f', '--format', help='set format of output')
    
    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser._optionals.title = 'options:'

    args = parser.parse_args()

    data1 = json.load(open(args.first_file))
    data2 = json.load(open(args.second_file))

if __name__ == '__main__':
    main()
