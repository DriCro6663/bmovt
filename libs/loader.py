import os

class Loader():
    """
    ファイルをロードするクラス
    
    Attributes
    ----------
    path: str
        読み込むファイルやディレクトリのパス
    """
    
    def __init__(self, path: str=os.getcwd()):
        """
        Parameters
        ----------
        path: str
            読み込むファイルやディレクトリのパス
        """
        self.path = os.path.abspath(path)
    
    def _read_file_name(self, path: str=None):
        """
        ファイルの名前を返す
        
        Parameters
        ----------
        path: str
            読み込むファイルのパス
        """
        if path is None: path = self.path
        return os.path.basename(path)
    
    def loadfile(self, path: str=None, encoding:str ="UTF-8"):
        """
        ファイルの読込
        
        Parameters
        ----------
        path: str, default: None
            読み込むファイルのパス
        encoding: str, default: None
            読み込むファイルのエンコーディング方式
            Ex. Unicode, UTF-8, Shift_JIS, 
        
        Returns
        -------
        data: str
            ファイルの中身
        """
        if path is None: path = self.path
        f = open(path, "r", encoding=encoding)
        data = f.read()
        f.close()
        return data
    
    def listdir(self, path: str=None, full_path: bool=False):
        """
        ディレクトリの内のファイルの名前
        
        Parameters
        ----------
        path: str
            読み込むディレクトリのパス
        full_path: bool
            絶対パスを返すか否か
        
        Returns
        -------
        files_name: list[str]
            ディレクトリの内のファイルやフォルダの名前のリスト
        """
        if path is None: path = self.path
        if full_path:
            files = [os.path.join(os.path.abspath(path), f) for f in os.listdir(path)]
        else:
            files = os.listdir(path)
        return files
    
    def listfiles(self, path: str=None, full_path: bool=False):
        """
        ディレクトリの内のファイルの名前の読込
        
        Parameters
        ----------
        path: str
            読み込むディレクトリのパス
        full_path: bool
            絶対パスを返すか否か
        
        Returns
        -------
        files_name: list[str]
            ディレクトリの内のファイルの名前のリスト
        """
        if path is None: path = self.path
        files = os.listdir(path)
        if full_path:
            files_file = [os.path.join(os.path.abspath(path), f) for f in files if os.path.isfile(os.path.join(path, f))]
        else:
            files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
        return files_file
    
    def listdirs(self, path: str=None, full_path: bool=False):
        """
        ディレクトリの内のフォルダの名前の読込
        
        Parameters
        ----------
        path: str
            読み込むディレクトリのパス
        full_path: bool
            絶対パスを返すか否か
        
        Returns
        -------
        files_name: list[str]
            ディレクトリの内のフォルダの名前のリスト
        """
        if path is None: path = self.path
        files = os.listdir(path)
        if full_path:
            files_dir = [os.path.join(os.path.abspath(path), f) for f in files if os.path.isdir(os.path.join(path, f))]
        else:
            files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
        return files_dir