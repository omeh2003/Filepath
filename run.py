import os
import sys
import MagicPath
import apkdecompiler
import apkutils2
import apkverify


class Prog:

    @classmethod
    def run(cls):
        defpath = MagicPath.FilePath(os.path.abspath(os.path.curdir))
        tmpdir1 =defpath.addpath("tmp1")
        tmpdir2 =defpath.addpath("tmp2")
        tmpdir1.ensure()
        tmpdir2.ensure()
        tmpdir1.addpath("2")
        file = defpath.addpath("apk.apk")
        apk= apkutils2.APK(file.path())
        res = apk.dex_files

        exit()






        pass


if __name__== "__main__":
    Prog.run()
