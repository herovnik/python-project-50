from gendiff.scripts import gendiff


def test_gendiff():
    file1 = "./tests/examples/file1.json"
    file2 = "./tests/examples/file2.json"
    result = format_value(stylish({
                '- follow': False,
                '  host': 'hexlet.io',
                '- proxy': '123.234.53.22',
                '- timeout': 50,
                '+ timeout': 20,
                '+ verbose': True
            }))
    assert gendiff.generate_diff(file1, file2) == result


def test_gendiff_yaml():
    file1 = "./tests/examples/file1.yaml"
    file2 = "./tests/examples/file2.yaml"
    result = format_value(stylish({
                '- follow': False,
                '  host': 'hexlet.io',
                '- proxy': '123.234.53.22',
                '- timeout': 50,
                '+ timeout': 20,
                '+ verbose': True
            }))
    assert gendiff.generate_diff(file1, file2) == result


def test_gendiff_req():
    file1 = "./tests/examples/filereq1.json"
    file2 = "./tests/examples/filereq2.json"
    result = format_value(stylish({'  common': 
                {'+ follow': False, 
                    '  setting1': 'Value 1',
                    '- setting2': 200, '- setting3': True,
                    '+ setting3': None,
                    '+ setting4': 'blah blah',
                    '+ setting5': {'key5': 'value5'},
                    '  setting6': {
                        '  doge': {
                            '- wow': '',
                            '+ wow': 'so much'},
                        '  key': 'value',
                        '+ ops': 'vops'
                    }
                }, 
                '  group1': {
                    '- baz': 'bas',
                    '+ baz': 'bars',
                    '  foo': 'bar',
                    '- nest': {
                        'key': 'value'
                        },
                    '+ nest': 'str'
                    }, 
                '- group2': {
                    'abc': 12345,
                    'deep': {
                        'id': 45
                    }
                }, 
                '+ group3': {
                    'deep': {
                        'id': {
                            'number': 45
                        }
                    }, 
                    'fee': 100500
                }
            }))
    assert gendiff.generate_diff(file1, file2) == result


def test_gendiff_plain():
    file1 = "./tests/examples/filereq1.json"
    file2 = "./tests/examples/filereq2.json"
    result = "Property 'common.follow' was added with value: false\n" \
            "Property 'common.setting2' was removed\n" \
            "Property 'common.setting3' was updated. From true to None\n" \
            "Property 'common.setting4' was added with value: 'blah blah'\n" \
            "Property 'common.setting5' was added with value: " \
            "[complex value]\n" \
            "Property 'common.setting6.doge.wow' was updated. " \
            "From '' to 'so much'\n" \
            "Property 'common.setting6.ops' was added with value: " \
            "'vops'\n" \
            "Property 'group1.baz' was updated. From 'bas' to 'bars'\n" \
            "Property 'group1.nest' was updated. From [complex value] to " \
            "'str'\n" \
            "Property 'group2' was removed\n" \
            "Property 'group3' was added with value: [complex value]"
    assert gendiff.generate_diff(file1, file2, form='plain') == result


def format_value(value, depth=0):
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
