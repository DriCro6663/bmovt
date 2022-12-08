import os

from bmovt.bmovt import *

if __name__ == "__main__":
    os.getcwd()
    bmovt = BmovT(
        config_path="./config/config.yaml", 
        loading_path="./res/loading_text.txt", 
        boot_path="./res/boot_text.txt", 
    )
    bmovt.output()