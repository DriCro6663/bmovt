# bmovt: Boot Movie Maker

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/DriCro6663/bmovt)
![GitHub](https://img.shields.io/github/license/DriCro6663/bmovt)

This is a program to make a video that looks like a boot screen of a retro computer.

## Introduction

[S-knife](https://commons.nicovideo.jp/users/1746455) like [computer boot screen-like thing (no effects_v1)](https://commons.nicovideo.jp/material/nc117696) as a reference.

I hereby express our gratitude for the abbreviation.

## Description

<iframe width="560" height="315" src="https://www.youtube.com/embed/lhHvjWNb8AA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

This is a program to make a video like that of a retro computer with the text that plays when the computer starts up.

## Demo

![bmovt_demo](./tests/boot_sample-min.gif)

## Usage

1. Download from [Release](https://github.com/DriCro6663/bmovt/releases) and extract the compressed file.
2. In the unzipped folder [./config/config.yaml](./config/config.yaml) in the extracted folder.

    ```yaml:config.yaml
    output_path: "./boot.mp4"                       # video_output_directory/video_name.mp4
    font_path: "./res/Myrica/Myrica.TTC"            # Font path
    width: 1920                                     # resolution horizontal
    height: 1080                                    # resolution vertical
    fps: 60                                         # FPS
    fourcc: "mp4a"                                  # Codec for video creation: . See /tests/fourcc_tag-mp4.txt
    crf: 16                                         # Video compression properties: 0 (quality: good, size: large) < crf < 64 (quality: bad, size: small)
    separator: !!python/str "=+\n+"                 # separator
    bg_color: !!python/tuple [0, 0, 0, 255]         # background color: tuple(r, g, b, a)
    font_color: !!python/tuple [255, 255, 255, 255] # font color: tuple(r, g, b, a)
    font_size: 32                                   # text size: pixels: https://www.linesmix.com/fonts.html
    spacing: 4                                      # Text spacing: pixels
    ````

3. Go to the unzipped folder [./res](./res) .
4. Edit [loading.txt](./res/loading_text.txt).

    ```python:loading.txt
    {
        # key: value, 
        0: [" "], 
        1: [" ", "."],
        2: ["/", "-", "\\"], 
        3: ["Loading", "Loading.", "Loading..", "Loading..."],
    }
    ```

5. Edit [boot_text.txt](./res/boot_text.txt).

    ```txt:boot_text
    First line: Settings for displaying the text.
    second and subsequent lines: text to display
    
    LOADING: Loading settings
        - TYPE    : display type of loading
                    Enter the key of loading.txt
                    If loading is not used, enter NONE
        - TIME    : Loading time
        - INTERVAL: display interval of loading characters
        - UNIT    : unit of TIME and INTERVAL
                    Enter "SEC" or "FRAME
    
    SHOW: Set display text
        - TYPE    : Display type of text
            - MOMENT   : Instantaneous
                         All text is displayed in one frame.
            - GRADUALLY: Gradually
                         Number of characters displayed : Number of characters / (TIME / INTERVAL)
            - L_BY_L   : Display characters per line
                         Read and process numbers in order of TIME, INTERVAL
                         TIME ! = 0: INTERVAL = TIME / number of line breaks 
                         INTERVAL ! = 0: TIME = INTERVAL * number of line breaks
            - F_BY_F   : Display one character per frame
        - TIME    : display time
        - INTERVAL: display interval
        - UNIT    : unit of TIME and INTERVAL
                      Enter "SEC" or "FRAME
    ````

6. Run the program to create a video.

## Requirement

* Windows 10
* Python 3.10
* conda 22.9.0

If you wish to edit the source code, please refer to the following to build your environment.

<details>
<summary>Please click here</summary>

### virtual_environment_build

```bash:Anaconda
conda create -n bmovt --file bmovt.yaml
```

If you need to configure proxy settings, please refer to the following.

````bash:Proxy
# windows.
# if you need to use proxy, please set proxy setting.
set HTTP_PROXY=http://<userid>:<password>@<server-address>:<port>
set HTTPS_PROXY=http://<userid>:<password>@<server-address>:<port>

# example
set HTTP_PROXY=http://proxy.example.com:8080
set HTTPS_PROXY=http://proxy.example.com:8080

# check proxy
echo %HTTP_PROXY% echo %HTTPS_PROXY
echo %HTTPS_PROXY%
````

### run

```bash
python -m bmovt
```

### py -> exe

Creating an executable file in Nuitka takes a long time (2 ~ 3 hours).

Also, Nuitka will ask if you want to install to C:\Users\UserName\AppData if you do not have GCC[MinGW64], please select [YES].

```bash:Nuitka
conda install -c conda-forge nuitka zstandard ordered-set -y

nuitka --mingw64 --follow-imports --onefile . /bmovt/__main__.py

$ nuitka3 --help
    --mingw64       : compile with mingw64, default: MSVC
    --follow-imports: include required modules in binary files
    --onefile       : combine binary files into one.
```

```bash:Pyinstaller
conda install -c conda-forge pyinstaller -y

pyinstaller . /bmovt/__main__.py --name [fileName] --onefile --icon [./img/icon.ico] --noconsole

$ pyinstaller --help
    --name     : specify exe file name
    --onefile  : combine exe files into one
    --noconsole: Suppress console display when running exe
    --debug all: debug output
    --clean    : delete cache
    --icon     : Specify the path to the icon file.
```

</details>

## Note

* Please note that at this time we do not have the ability to automatically break long strings into new lines.
* Since ffmpeg is used, if you have not added it to the environment variable, please install it and pass it through the path.

```bash:ffmpeg
conda install -c conda-forge ffmpeg
```

## Updates

* 2022/12/09:<br>[v0.0.1](https://github.com/DriCro6663/bmovt/releases/tag/v0.0.1) was released.

## Author

* [Github DriCro6663](https://github.com/DriCro6663)
* [Twitter Dri_Cro_6663](https://twitter.com/Dri_Cro_6663)
* [YouTube -DriCro-](https://www.youtube.com/channel/UCyWgav9wdiPVjYphB7jrWCQ)
* [PieceX DriCro6663](https://www.piecex.com/users/profile/DriCro6663)
* [Dri-Cro's Memorandum](https://dri-cro-6663.jp/)
* dri.cro.6663@gmail.com

## License

Please check the [LICENSE](.LICENSE) file.
