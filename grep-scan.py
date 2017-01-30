# /usr/bin/env python
# -*- coding: utf-8 -*-
#
# By @proclnas

import requests
import os
import argparse
import sys
import re
from threading import Thread, Event, Lock
from Queue import Queue
requests.packages.urllib3.disable_warnings()


class GrepScan:
    def __init__(self, uri_file, output, pattern, threads):
        self.uri_file = uri_file
        self.output = output
        self.pattern = pattern
        self.q = Queue()
        self.t_stop = Event()
        self.threads = threads
        self.list_size = len(open(self.uri_file).readlines())
        self.counter = 0
        self.terminal = sys.stdout
        self.lock = Lock()

    def save_buf(self, content):
        '''
        Save buf to file
        '''
        with open(self.output, 'a+') as fp:
            fp.write('{}\n'.format(content.encode("UTF-8")))

    def search(self, q):
        '''
        Search in the uri the given pattern
        '''
        while not self.t_stop.is_set():
            self.t_stop.wait(1)

            try:
                uri = q.get()

                with self.lock:
                    self.terminal.write('[GET] {}\n'.format(uri))

                r = requests.get(
                    uri,
                    verify=False
                )

                if re.search(self.pattern, r.text):
                    with self.lock:
                        self.terminal.write(
                            '[+][Pattern found] {}\n'.format(uri)
                        )

                        with open(self.output, 'r') as fp:
                            fp.write('{}\n'.format(uri))
            except:
                pass
            finally:
                self.counter += 1
                q.task_done()

    def start(self):
        '''
        Launch threads
        '''
        print 'Scanning...'

        for _ in xrange(self.threads):
            t = Thread(target=self.search, args=(self.q,))
            t.setDaemon(True)
            t.start()

        for cred in open(self.uri_file):
            self.q.put(cred.strip())

        try:
            while not self.t_stop.is_set():
                self.t_stop.wait(1)
                if self.counter == self.list_size:
                    self.t_stop.set()

        except KeyboardInterrupt:
            print '~ Sending signal to kill threads...'
            self.t_stop.set()
            sys.exit(0)

        self.q.join()
        print 'Finished!'


if __name__ == "__main__":
    banner = '''

 ####  #####  ###### #####         ####   ####    ##   #    #
#    # #    # #      #    #       #      #    #  #  #  ##   #
#      #    # #####  #    # #####  ####  #      #    # # #  #
#  ### #####  #      #####             # #      ###### #  # #
#    # #   #  #      #            #    # #    # #    # #   ##
 ####  #    # ###### #             ####   ####  #    # #    #
by @proclnas
    '''

    parser = argparse.ArgumentParser(
        description='Grep scan'
    )

    parser.add_argument(
        '-f', '--file',
        action='store',
        dest='uri_file',
        help='uri file'
    )

    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output',
        help='Output to save valid results',
        default='output.txt'
    )

    parser.add_argument(
        '-t', '--threads',
        action='store',
        default=1,
        dest='threads',
        help='Concurrent workers',
        type=int
    )

    parser.add_argument(
        '-p', '--pattern',
        action='store',
        default=1,
        dest='pattern',
        help='(String: \'foo\' or a regexp: \'foo|bar\''
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    if not args.uri_file:
        print banner
        exit(parser.print_help())

    if not os.path.isfile(args.uri_file):
        exit('File {} not found'.format(args.dork_file))

    print banner
    grep_scan = GrepScan(
        args.uri_file,
        args.output,
        args.pattern,
        args.threads
    )
    grep_scan.start()
