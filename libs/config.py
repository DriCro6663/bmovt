# coding: utf-8
import json
import yaml
import configparser
from configparser import ConfigParser

# ファイルの存在チェック用モジュール
import os
import errno

class Config_ini():
    """
    設定ファイル管理モジュール
    url: https://qiita.com/mimitaro/items/3506a444f325c6f980b2
    
    Attributes
    ----------
    path: str
        読み込むファイルのパス
    config: class
        configparser.ConfigParser
    """
    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path: str
            読み込むファイルのパス
        """
        self.path = os.path.abspath(path)
        self.config = None
        self.load_ini()
    
    def load_ini(self, path: str=None):
        """
        config ファイルの読込
        
        Parameters
        ----------
        path: str, default: None
            読み込むファイルのパス
        """
        if path is None:
            path = self.path
        
        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        
        # ini ファイルの読み込み
        config = configparser.ConfigParser()
        self.config = config.read(path, encoding="utf-8")
    
    def sections(self):
        """
        セクション要素の取得
        ※ DEFAULT セクションは表示されない
        
        Returns
        -------
        sections: list
            セクション名の一覧
        """
        return self.config.sections()
    
    def items(self, name: str):
        """
        セクション要素の取得
        
        Parameters
        ----------
        name: str
            セクションの名前
        
        Returns
        -------
        sections: list
            セクションの要素
        """
        return self.config.items(name)

class Config_json():
    """
    config.json 管理モジュール
    
    Attributes
    ----------
    path: str, default: "../config.json"
        読み込むファイルのパス
    config: dict
        config の中身
    """
    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path: str
            読み込むファイルのパス
        """
        self.path = os.path.abspath(path)
        self.config = self.load_json()
    
    def load_json(self, path: str=None):
        """
        config ファイルの読込
        
        Parameters
        ----------
        path: str, default: None
            読み込むファイルのパス
        
        Returns
        -------
        config: list
            config ファイルの中身
        """
        if path is None:
            path = self.path
        
        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        
        json_file = open(path, "r", encoding="utf-8")
        config = json.load(json_file)
        json_file.close()
        return config

class Config_yaml():
    """
    config.json 管理モジュール
    url: https://kokiblog.com/2019/08/21/python_yaml/
    
    Attributes
    ----------
    path: str
        読み込むファイルのパス
    config: dict
        config の中身
    """
    def __init__(self, path: str):
        """
        Parameters
        ----------
        path: str
            読み込むファイルのパス
        """
        self.path = os.path.abspath(path)
        self.config = self.load_yaml()
    
    def load_yaml(self, path: str=None):
        """
        config ファイルの読込
        
        Parameters
        ----------
        path: str, default: None
            読み込むファイルのパス
        
        Returns
        -------
        config: list
            config ファイルの中身
        """
        if path is None:
            path = self.path
        
        # 指定したファイルが存在しない場合、エラー発生
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        
        yaml_file = open(path, "r", encoding="utf-8")
        config = yaml.full_load(yaml_file.read())
        yaml_file.close()
        return config

class Config(
    Config_ini, Config_json, Config_yaml
):
    """
    config 管理モジュール
    ini, json, yml, yaml, 
    
    Attributes
    ----------
    path: str
        読み込むファイルのパス
    config: dict
        config の中身
    """
    def __init__(self, path: str) -> None:
        """
        Parameters
        ----------
        path: str
            読み込むファイルのパス
        """
        path = os.path.abspath(path)
        # 指定したファイルが存在しない場合、エラー発生
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        root, ext = os.path.splitext(path)
        if ext == ".ini":
            Config_ini.__init__(self, path=path)
        elif ext == ".json":
            Config_json.__init__(self, path=path)
        elif (ext == ".yml") or (ext == ".yaml"):
            Config_yaml.__init__(self, path=path)
        else:
            pass