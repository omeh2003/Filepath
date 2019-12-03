# Filepath
Pathless library python3 . Very easy. 

        dir = MagicPath.FilePath(os.path.abspath(os.path.curdir))     
        tmpdir1 = dir.addpath("tmp1")
        tmpdir2 = dir.addpath("tmp2")
        dir.is_dir() == True
        dir.ls()
        dir.findfile()
        tmpdir1.ensure()
        tmpdir2.ensure()
        tmpdir1.addpath("2")
        dir.rmtree()`
        


