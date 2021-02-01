from util.chinaz import chinaz
from util.Brute import BruteDir
import common

if __name__ == '__main__':
    domain = input('请输入要查询的域名:')

    c = chinaz(domain=domain)
    c.run()

    print('开始暴力破解子域名')
    b = BruteDir(domain=domain)
    b.brutedir()
    print('暴力破解结束')

    print('正在整理子域名信息')
    common.merge_result(domain)
    print('整理结束')


