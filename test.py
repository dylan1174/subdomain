import time
import common
import json

if __name__ == '__main__':
    result_file = ['chinaz.json', 'brute.json']
    result_path = []
    subdomain = []
    domain = '163.com'
    for r in result_file:
        result_path.append(common.get_result(domain=domain, type=r))
    for p in result_path:
        with open(p, 'r') as f:
            res = json.load(f)
            subdomain.extend(res)
    subdomain = list(set(subdomain))

    common.save_result(filename=common.get_result(domain=domain, type='result.json'), subdomains=subdomain)



