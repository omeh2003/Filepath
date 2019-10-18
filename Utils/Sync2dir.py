"""
Скрипт для rsynca двух каталогов с рекурсивным обходом.
Не добавляет то что уже есть в каталоге назначения.
Для работы с путями используется MagicPath
"""
import os

from dirsync import sync

import MagicPath

source_dir = "/home/user/dir/git"
dest_dir = "/home/user/git"


class Prog:

    @classmethod
    def run(cls):
        sourcedir = MagicPath.FilePath(os.path.abspath(source_dir))
        targetdir = MagicPath.FilePath(os.path.abspath(dest_dir))
        listdirs = sourcedir.ls_dir()
        print(listdirs.__len__())
        sourcedirs = []
        for dirr in listdirs:
            print(dirr)
            if not dirr.basename() == "_iso" and not dirr.basename()[0] == "$" and not dirr.basename()[0] == ".":
                sourcedirs.append(dirr)

        print(sourcedirs.__len__())
        for source in sourcedirs:
            if source.ls().__len__() < 1:
                print(source.basename())
                print("Not file")
                continue
            if targetdir.addpath(source.basename()).is_dir():
                print(source.basename())
                print("Is already in dest")
                continue
            print(source.path())
            sync(source.path(), targetdir.addpath(source.basename()).path(), 'sync', create=True)


if __name__ == "__main__":
    Prog.run()
