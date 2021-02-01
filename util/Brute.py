from dns import resolver
import queue
import os
import common
import threading
import sys
import time


class BruteDir(object):
    def __init__(self, domain):
        self.domain = domain

    def brutedir(self):
        st = time.time()
        print('开始爆破子域名{}'.format(time.strftime('%X')))
        threads = []
        result = []
        thread_count = 2000
        q = queue.Queue()
        path = os.path.join(common.get_root_path(), 'dir\dic.txt')
        with open(path, 'r') as f:
            r = f.readlines()
        for i in r:
            i = i.strip('\n')
            url = '{subdomain}.{domain}'.format(subdomain=i, domain=self.domain)
            q.put(url)

        total = q.qsize()
        for i in range(thread_count):
            threads.append(self.Brute(q, result, total))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        path = common.get_result(domain=self.domain, type='brute.json')
        common.save_result(path, result)
        print('\n爆破结束{}  共计用时{:.2f}s'.format(time.strftime('%X'), time.time() - st))

    class Brute(threading.Thread):
        def __init__(self, q, result, total):
            threading.Thread.__init__(self)
            self.q = q
            self.result = result
            self.total = total

        def run(self) -> None:
            while not self.q.empty():
                url = self.q.get()
                self.msg()
                try:
                    A = resolver.resolve(url, 'A')
                    if A.response.answer:
                        self.result.append(url)
                except Exception:
                    pass

        def msg(self):
            left = self.q.qsize()
            total = self.total
            per = ((total - left) / total) * 100
            sys.stdout.write('\r{} left {} total|{:.2f}% scan'.format(left, total, per))




