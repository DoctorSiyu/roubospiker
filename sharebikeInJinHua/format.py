# coding: utf-8
import fileinput
import io
import sys
import chardet
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def format(line):
    """
    :param line:
    :return:
    """
    result = {}
    tmp = eval(line.decode('utf-8'))
    try:
        result = {
            "bikeid": str(tmp["distId"]),
            "lat": tmp["distY"],
            "lng": tmp["distX"],
            "type" : 'mb'
        }

        print(str(result).strip(), flush=True)

    except Exception as e:
        print(e)
        pass


def main():
    try:
        for line in fileinput.input(mode='rb'):
            format(line)
        sys.stderr.close()
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    main()
