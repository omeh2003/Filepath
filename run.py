import os
import sys
from pprint import pprint

import MagicPath

import instagram_explore.explore as im

a = im.user("sashazvereva", 100)

pprint(a)


class Prog:

    @classmethod
    def run(cls):
        d = MagicPath.FilePath(os.path.abspath(os.path.curdir))
        tmpdir1 = d.addpath("tmp1")
        tmpdir2 = d.addpath("tmp2")
        tmpdir1.ensure()
        tmpdir2.ensure()
        tmpdir1.addpath("2")
        file = d.addpath("apk.apk")
        apk = apkutils2.APK(file.path())
        res = apk.dex_files()

        exit()

        pass


if __name__ == "__main__":
    Prog.run()
