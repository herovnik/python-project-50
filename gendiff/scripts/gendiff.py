import argparse
import json

import yaml


def main():
    parser = argparse.ArgumentParser(
                        prog='gendiff',
                        description='Compares two configuration" \
                        "files and shows a difference')

    parser.add_argument('-f', '--format', choices=['json', 'plain'], 
                        help='set format of output')
    
    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser._optionals.title = 'options:'

    args = parser.parse_args()

    print(generate_diff(
                args.first_file,
                args.second_file,
                form=args.format
            )
        )


def generate_diff(file_path1, file_path2, form=None):
    if file_path1.endswith(".json"):
        data1 = dict(sorted(dict(json.load(open(file_path1))).items()))
        data2 = dict(sorted(dict(json.load(open(file_path2))).items()))
    if file_path1.endswith(".yaml") or file_path1.endswith(".yml"):
        data1 = dict(sorted(dict(yaml.safe_load(open(file_path1))).items()))
        data2 = dict(sorted(dict(yaml.safe_load(open(file_path2))).items()))
    
    if not form:
        return format_value(stylish(generate_req_diff(data1, data2)))
    if form == 'plain':
        return plain_diff(data1, data2)
    if form == 'json':
        return json.dumps(generate_req_diff(data1, data2), indent=4)

    
def generate_req_diff(data1, data2):
    keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff = {}

    for key in keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if key not in data1:
            diff[f"+ {key}"] = val2
        elif key not in data2:
            diff[f"- {key}"] = val1
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff[f"  {key}"] = generate_req_diff(val1, val2)
        elif val1 == val2:
            diff[f"  {key}"] = val1
        else:
            diff[f"- {key}"] = val1
            diff[f"+ {key}"] = val2
            
    return diff


def plain_diff(data1, data2):
    def format_value(value):
        if isinstance(value, dict):
            return "[complex value]"
        if isinstance(value, str):
            return f"'{value}'"
        return str(value).lower() if isinstance(value, bool) else str(value)

    def compare_dicts(old_dict, new_dict, path=""):
        lines = []
        keys = sorted(set(old_dict.keys()) | set(new_dict.keys()))

        for key in keys:
            current_path = f"{path}.{key}" if path else key
        
            old_val = old_dict.get(key)
            new_val = new_dict.get(key)

            if key in old_dict and key not in new_dict:
                lines.append(f"Property '{current_path}' was removed")
        
            elif key not in old_dict and key in new_dict:
                lines.append(
                    f"Property '{current_path}' "
                    f"was added with value: {format_value(new_val)}"
                )
        
            elif isinstance(old_val, dict) and isinstance(new_val, dict):
                lines.extend(compare_dicts(old_val, new_val, current_path))
        
            elif old_val != new_val:
                lines.append(f"Property '{current_path}' was updated. " 
                    f"From {format_value(old_val)} " 
                    f"to {format_value(new_val)}"
                    )

        return lines
    result = compare_dicts(data1, data2)
    return result


def format_value(value, depth):
    if isinstance(value, dict):
        indent = '    ' * (depth + 1)
        bracket_indent = '    ' * depth
        lines = []
        for k, v in value.items():
            lines.append(f'{indent}{k}: {format_value(v, depth + 1)}')
        return '{\n' + '\n'.join(lines) + '\n' + bracket_indent + '}'
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    return str(value)


def stylish(diff, depth=1):
    bracket_indent = '    ' * (depth - 1)
    lines = []

    for raw_key, value in diff.items():
        prefix = raw_key[:2]
        key = raw_key[2:]

        symbol = prefix.strip()
        sign = f'{symbol} ' if symbol else '  '
        line_indent = f'{bracket_indent}  {sign}'

        if isinstance(value, dict) and any(
            k.startswith(('+ ', '- ', '  ')) for k in value
        ):
            formatted = stylish(value, depth + 1)
        else:
            formatted = format_value(value, depth)

        lines.append(f'{line_indent}{key}: {formatted}')

    return '{\n' + '\n'.join(lines) + '\n' + bracket_indent + '}'



if __name__ == '__main__':
    main()
