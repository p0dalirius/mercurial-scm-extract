#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : mercurial-scm-extract.py
# Author             : Podalirius (@podalirius_)
# Date created       : 19 Feb 2023

import argparse
import os
import requests


VERSION = "1.1"



class MercurialSCMExtractor(object):
    """
    Documentation for class MercurialSCMExtractor
    """

    default_files = [
        "/.hg/store/fncache",
        "/.hg/store/phaseroots",
        "/.hg/store/undo.phaseroots",
        "/.hg/store/undo.backupfiles",
        "/.hg/store/undo",
        "/.hg/store/00manifest.i",
        "/.hg/store/00changelog.i",
        "/.hg/store/requires",
        "/.hg/undo.backup.dirstate",
        "/.hg/undo.branch",
        "/.hg/last-message.txt",
        "/.hg/undo.desc",
        "/.hg/undo.bookmarks",
        "/.hg/wcache/checknoexec",
        "/.hg/wcache/checklink-target",
        "/.hg/wcache/manifestfulltextcache",
        "/.hg/wcache/checkisexec",
        "/.hg/cache/rbc-revs-v1",
        "/.hg/cache/rbc-names-v1",
        "/.hg/cache/branch2-served",
        "/.hg/undo.dirstate",
        "/.hg/dirstate",
        "/.hg/requires",
        "/.hg/00changelog.i"
    ]

    def __init__(self, dump_dir, verbose):
        super(MercurialSCMExtractor, self).__init__()
        self.verbose = verbose
        self.dump_dir = dump_dir
        self.todo_dump = []

    def extract(self, url):
        if not os.path.exists(self.dump_dir):
            os.makedirs(self.dump_dir, exist_ok=True)
        print("[+] Extracting %d default mercurial files:" % len(self.default_files))
        self.__dump_files(url, self.default_files)
        print()

        # Parse useful files:
        if os.path.exists(self.dump_dir+"/.hg/store/fncache"):
            project_files = []
            cache_project_files = []
            f = open(self.dump_dir+"/.hg/store/fncache", "r")
            for line in f.readlines():
                if line.startswith("data/"):
                    store_filename = ""
                    original_name = line[5:].strip()[:-2]
                    project_files.append("/" + original_name)
                    for char in line[5:].strip():
                        if char == char.upper() and char.isalpha():
                            store_filename += "_" + char.lower()
                        else:
                            store_filename += char
                    cache_project_files.append("/.hg/store/data/" + store_filename)
            print("[+] Extracting mercurial cache of %d project files:" % len(cache_project_files))
            self.__dump_files(url, cache_project_files)
            print()

            print("[+] Extracting %d project files:" % len(project_files))
            self.__dump_files(url, project_files)
            print()

        print("[+] All done!")

    def __dump_files(self, url, files, verbose=False):
        def convert_filesize(contentsize):
            units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
            for k in range(len(units)):
                if contentsize < (1024 ** (k + 1)):
                    break
            return "%4.2f %s" % (round(contentsize / (1024 ** (k)), 2), units[k])
        #
        for file in files:
            r = requests.get(url + file, verify=False)
            if r.status_code == 200:
                dumped_file = self.dump_dir+file
                if not os.path.exists(os.path.dirname(dumped_file)):
                    os.makedirs(os.path.dirname(dumped_file), exist_ok=True)
                size = convert_filesize(int(r.headers["Content-Length"]))
                print("  | \x1b[92m[+] (%9s) Dumped: %s\x1b[0m" % (size, file))
                f = open(dumped_file, "wb")
                f.write(r.content)
                f.close()
            else:
                if self.verbose:
                    print("  | \x1b[91m[!] (==error==) Could not dump: %s\x1b[0m" % file)


def parseArgs():
    print("mercurial-scm-extract.py v%s - by @podalirius_\n" % VERSION)

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-u", "--url", default=None, required=True, help='Target URL.')
    parser.add_argument("-d", "--dir", default=None, required=True, help='Directory where to save dumped files.')

    parser.add_argument("-k", "--insecure", action="store_true", default=False, help="Allow insecure server connections when using SSL (default: False)")

    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    if options.insecure:
        # Disable warings of insecure connection for invalid certificates
        requests.packages.urllib3.disable_warnings()
        # Allow use of deprecated and weak cipher methods
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            pass

    try:
        r = requests.head(options.url, verify=False)
    except Exception as e:
        print("[!] Error: %s" % e)
        print("[!] Target is down. Stopping ...")
    else:
        m = MercurialSCMExtractor(
            dump_dir=options.dir,
            verbose=options.verbose
        )
        m.extract(url=options.url)
