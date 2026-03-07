import argparse
import json


def main():
    parser = argparse.ArgumentParser(
                        prog='gendiff',
                        description='Compares two configuration" \
                        "files and shows a difference')

    parser.add_argument('-f', '--format', help='set format of output')
    
    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser._optionals.title = 'options:'

    args = parser.parse_args()

    data1 = dict(json.load(open(args.first_file)))
    data2 = dict(json.load(open(args.second_file)))
    
    print(data1)
    print(data2)

    print(generate_diff(args.first_file, args.second_file))


def generate_diff(file_path1, file_path2):
    data1 = dict(sorted(dict(json.load(open(file_path1))).items()))
    data2 = dict(sorted(dict(json.load(open(file_path2))).items()))
    result = {}
    for i in data1:
        if data1.get(i, None) == data2.get(i, None):
            result[i] = data1[i]
        if data1.get(i, None) != data2.get(i, None):
            result[f"- {i}"] = data1[i]
            if data2.get(i, None) is not None:
                result[f"+ {i}"] = data2[i]
    for j in data2:
        if data1.get(j, None) is None:
            result[f"+ {j}"] = data2[j]
    return result


if __name__ == '__main__':
    main()
