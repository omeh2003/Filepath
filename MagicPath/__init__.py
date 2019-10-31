import datetime
import os
import random as rnd
import re
import shutil
from enum import Enum


class SortOrder(Enum):
    """
    сортировка  для функции LS

    """
    RANDOM = 1
    ORDER = 2
    DATE = 3
    ALPHA = 4


class FilePath(object):
    """
            Обертка для файлов и каталогов
    """

    def __init__(self, mpath):
        super().__init__()
        self.mpath = mpath

    def __add__(self, other):
        """
             Объединяет два пути
        """
        if isinstance(other, str):
            other = FilePath(other)
        return FilePath(os.path.join(self.mpath, other.mpath))

    def ls(self, filetype="", order=SortOrder.ALPHA, hourly=False):
        """
        Содержимое каталога

        :param filetype: ext
        :param order: how to sort the output
        :param hourly: whether should pick one file per hour (used for debug)
        :return: list of FilePathes
        """

        mlist = os.listdir(self.mpath)

        if order == SortOrder.RANDOM:
            # случайная сортировка (используется для выбора случайных каталогов)
            rnd.shuffle(mlist)
        elif order == SortOrder.ORDER:
            # порядок по первому номеру в имени файла (для отладки)
            mlist.sort(key=lambda e: int(re.match(r"^(\d+)_.*", os.path.basename(e)).group(1)))
        elif order == SortOrder.DATE:
            # order by the timestamp in file name (for debug)
            mlist.sort(key=lambda e: int(re.match(r"^.*_(\d+)\.json", os.path.basename(e)).group(1)))
        elif order == SortOrder.ALPHA:
            # по алфавиту
            mlist.sort()

        if hourly:
            new_res = []
            last_picked = set()
            for fn in mlist:
                ts = int(re.match(r"^.*_(\d+)\.json", os.path.basename(fn)).group(1))
                city = re.match(r"(\d+)_([a-zA-Z]+)_.*", os.path.basename(fn)).group(2)
                d = datetime.datetime.fromtimestamp(ts).replace(minute=0, second=0, microsecond=0)
                if (city, d) not in last_picked:
                    last_picked.add((city, d))
                    new_res.append(fn)
            mlist = new_res

        res = [FilePath(os.path.join(self.mpath, f)) for f in mlist]
        res1 = []
        if filetype.__len__() > 1:
            for r in res:
                if r.is_file() and r.ext() == filetype:
                    res1.append(r)
            res = res1
        return res

    def ls_dir(self, filetype="", order=SortOrder.ALPHA, hourly=False):
        return [d for d in self.ls() if d.is_dir()]

    def ensure(self):
        """
            Проверка, что каталог, описанный в этом пути существует
        """
        if not os.path.exists(self.mpath):
            os.makedirs(self.mpath)

    def open(self, mode='r'):
        """
        Открыть файл
        :return: FilePathWithHelper для использования "with"
        """
        return FilePathWithHelper(self, mode)

    def rmtree(self):
        """
        Удалить каталог рекурсивно
        """
        shutil.rmtree(self.mpath)

    def rm(self):
        """
        Удалить
        """
        os.remove(self.mpath)

    def basename(self):
        """
        Имя каталога или файла
        """
        return os.path.basename(self.mpath)

    def path(self):
        """
        Полный путь
        """
        return self.mpath

    def find_files(self):
        """
        поиск всех файлов
        """
        for dir, subdirs, files in os.walk(self.mpath):
            dfp = fp(dir)
            for f in files:
                yield dfp + fp(f)

    def find_files_item(self, file):
        """
        Найти файл
        """
        _file = file
        _list=list(FilePath.find_files(self))
        if any(_file in s.basename() for s in _list.__iter__()):
            return True
        return False



    def is_dir(self):
        return self.exist() and os.path.isdir(self.mpath)

    def is_file(self):
        return self.exist() and os.path.isfile(self.mpath)

    def exist(self):
        try:
            return os.path.exists(self.mpath)
        except Exception as ex:
            return False

    def ext(self):
        if self.is_dir():
            raise Exception("Illegal operation extension for directory")
        sp = self.basename().split(".")
        if len(sp) == 1:
            return ''
        return sp[-1]

    def __str__(self):
        return self.path()

    def __unicode__(self):
        return self.path()

    def addpath(self, *args):
        obj = FilePath(os.path.abspath(os.path.join(self.path(), *args)))

        return obj

    def me_copy_to(self, object):
        if object.is_file() and self.is_file():
            file = self.path()
            os.remove(self.path())
            shutil.copy2(object.path(), file)
            return FilePath(object.path())
        if object.is_file() and self.is_dir():
            shutil.copy2(object.path(), self.path())
            return FilePath(os.path.abspath(os.path.join(self.path(), object.basename())))
        if self.is_dir() and not object.exist():
            object.ensure()
            self.me_copy_to(object)
        if self.is_dir() and object.is_dir():
            copytreepath(self.path(), object.path(), False, True)
        if self.is_file() and object.is_dir():
            file = self.basename()
            shutil.copy2(self.path(), object.addpath(file).path())
            return object.addpath(file)

    def me_move(self, object):
        new = self.me_copy_to(object)
        if self.is_dir():
            self.rmtree()
        if self.is_file():
            self.rm()
        if new.exist():
            return new
        raise Exception


class FilePathWithHelper(object):

    def __init__(self, filepath, mode):
        super().__init__()
        self.fp = filepath
        self.mode = mode

    def __enter__(self):
        self.fd = open(self.fp.mpath, mode=self.mode)
        return self.fd

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()


def fp(mpath):
    """
    Alias for FilePath constructor
    """
    if isinstance(mpath, FilePath):
        return FilePath(mpath.mpath)
    return FilePath(mpath)


def copytreepath(src, dst, symlinks=False, ignore=None):
    for item in src.ls():
        s = src.addpath(item.basename())
        d = dst.addpath(item.basename())
        if s.is_dir() and not d.exist() :
            shutil.copytree(s.path(), d.path(), ignore=None)
        else:
            if not d.exist():
                shutil.copy2(s.path(), d.path())
