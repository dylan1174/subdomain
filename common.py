import json
from random import choice
import os

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
]


def get_header():
    header = {
        'user-agent': choice(USER_AGENTS),
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9'
    }
    return header


# 返回一个result的路径 文件名为查询的方式+json后缀
def get_result(domain, type):
    dirpath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dirpath, 'result\{}'.format(domain))
    if not os.path.exists(path):
        os.makedirs(path)
    _cache_path = os.path.join(path, type)
    return _cache_path


def get_root_path():
    path = os.path.dirname(os.path.abspath(__file__))
    return path


def save_result(filename: str, subdomains: list):
    with open(filename, 'w') as f:
        json.dump(subdomains, f, indent=4)


def merge_result(domain):
    result_file = ['chinaz.json', 'brute.json']
    result_path = []
    subdomain = []
    for r in result_file:
        result_path.append(get_result(domain=domain, type=r))
    for p in result_path:
        with open(p, 'r') as f:
            res = json.load(f)
            subdomain.extend(res)
    subdomains = list(set(subdomain))

    save_result(filename=get_result(domain=domain, type='result.json'), subdomains=subdomains)



