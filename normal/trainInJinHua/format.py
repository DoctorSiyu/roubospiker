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
            "name": str(tmp["name"]),
            "lat": tmp["location"]["lat"],
            "lng": tmp["location"]["lng"],
            "address": str(tmp["address"]),
            "tag": str(tmp["detail_info"]["tag"]),
        }

        # 部分数据可能缺失字段
        if "detail_url" in tmp["detail_info"]:
            result["detail_url"] = tmp["detail_info"]["detail_url"]
        else:
            result["detail_url"] = ""

        if "overall_rating" in tmp["detail_info"]:
            result["rate"] = tmp["detail_info"]["overall_rating"]
        else:
            result["rate"] = "0.0"

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
