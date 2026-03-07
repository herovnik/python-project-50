from gendiff.scripts import gendiff


def test_gendiff():
    file1 = "/home/nikon/test/edu/projects/python-project-50/" \
    "gendiff/examples/file1.json"
    file2 = "/home/nikon/test/edu/projects/python-project-50/" \
    "gendiff/examples/file2.json"
    result = {
                '- follow': False,
                'host': 'hexlet.io',
                '- proxy': '123.234.53.22',
                '- timeout': 50,
                '+ timeout': 20,
                '+ verbose': True
            }
    assert gendiff.generate_diff(file1, file2) == result
