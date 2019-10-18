import os
import sys
import MagicPath

class Prog:

    @classmethod
    def run(cls):
        defpath = MagicPath.FilePath(os.path.abspath(os.path.curdir))
        tmpdir1 =defpath.addpath("tmp1")
        tmpdir2 =defpath.addpath("tmp2")
        tmpdir1.ensure()
        tmpdir2.ensure()
        tmpdir1.addpath("2")
        MagicPath.copytreepath(tmpdir1,tmpdir2)
        res= tmpdir2.find_files_item("javacToTranslate_v1.1.7z")
        print(res)




        pass


if __name__== "__main__":
    Prog.run()
