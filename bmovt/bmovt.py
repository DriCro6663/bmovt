import os
import sys
from pathlib import Path
parent_dir = str(Path().resolve())
ffmpeg_dir = os.path.join(parent_dir, "res/ffmpeg/bin")
sys.path.append(parent_dir)
sys.path.append(ffmpeg_dir)
os.chdir(parent_dir)

from libs import *
from .libs import *

import re
import subprocess
from tqdm import tqdm
import ffmpeg
import cv2
from PIL import Image, ImageDraw, ImageFont

class BmovT(Config, Loader):
    """
    レトロパソコンのブート画面のような文字列動画を出力
    
    Attributes
    ----------
    output_path: str, default: ".../"
        動画の出力先パス
    font_path: str, default: ".../res/Myrica/Myrica.TTC"
        フォントのパス
    width: int
        動画の横幅 [px]
    height: int
        動画の縦幅 [px]
    fps: int
        動画のFPS
    fourcc: str
        動画作成時のコーデック
        bmobt/tests/fourcc_tag-mp4.txt を参照
    crf: int
        ffmpeg を使用した動画の圧縮プロパティ
        0(品質：良, サイズ：大) < crf < 64(品質：悪, サイズ：小)
    separator: str
        区切り文字
    bg_color: tuple(r, g, b, a), default: (0, 0, 0, 0)
        バックグラウンドの色
    font_color: tuple(r, g, b, a), default: (255, 255, 255, 255)
        フォントの色
    font_size: float, default: 32 px
        フォントのサイズ
    spacing: float, default: 4 px
        テキストの行間
    bg: Image.new
        背景画像の配列
    font: ImageFont.truetype
        テキストのフォントの設定
    interval_sec: float, default: 0.1
        デフォルトのインターバル秒
    interval_frame: int, default: 5
        デフォルトのインターバルフレーム
    video: cv2.VideoWriter
        動画作成器
        cv2.VideoWriter()
    displayed_text: str, default: ""
        表示したテキスト
    """
    def __init__(
            self, config_path: str="../config/mov_conf.yml", 
            loading_path: str="../res/loading_text.txt", 
            boot_path: str="../res/boot_text.txt", 
        ) -> None:
        """
        Parameters
        ----------
        config_path: str, default: "../config/mov_conf.yml"
            設定ファイルのパス
        loading_path: str, default: "../res/loading_text.txt"
            ローディングテキストのパス
        boot_path: str, default: "../res/boot_text.txt"
            ブートテキストのパス
        """
        self._load_config(path=os.path.abspath(config_path))
        self._load_loading_text(path=os.path.abspath(loading_path))
        self._load_boot_text(path=os.path.abspath(boot_path))
        
        self.bg = Image.new("RGBA", self.size, self.bg_color)
        self.font = ImageFont.truetype(self.font_path, self.font_size)
        
        self.interval_sec = 0.1
        self.interval_frame = 5
        
        #gstreamer_str = f"gst-launch-1.0 -e -v autovideosrc ! decodebin ! videoconvert ! x264enc ! mp4mux ! filesink location={self.output_path}"
        #self.video  = cv2.VideoWriter(gstreamer_str, 0, self.fps, self.size)
        fourcc = cv2.VideoWriter_fourcc(*self.fourcc) # コーデックの指定
        self.video  = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.size)
        self.displayed = ""
    
    def _load_config(self, path: str):
        """
        設定ファイルの読込
        
        Parameters
        ----------
        path: str
            設定ファイルのパス
        """
        c = Config(path=path)
        for k, v in c.config.items():
            setattr(self, k, v)
        self.size = (self.width, self.height)
    
    def _load_loading_text(self, path: str):
        """
        ローディングテキストの読込
        
        Parameters
        ----------
        path: str
            ローディングテキストのファイルのパス
        """
        l = Loader()
        data = l.loadfile(path=path)
        self.loading_text = eval(data)
    
    def _load_boot_text(self, path: str):
        """
        ブートテキストの読込
        
        Parameters
        ----------
        path: str
            ブートテキストのファイルのパス
        """
        l = Loader()
        data = l.loadfile(path=path)
        data = re.split(self.separator, data)
        self.boot_cfg = [eval(d.splitlines()[0]) for d in data]
        self.boot_txt = ["".join(d.splitlines(True)[1:]) for d in data]
    
    def _draw_text(self, text: str, interval: int=0, add_text: bool=True):
        """
        バックグランド画像にテキストを書き込む
        
        ImageDraw.text(): https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.text
        Text anchors: https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors
        ImageDraw.textbbox(): https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.textbbox
        
        Parameters
        ----------
        text: str
            書き込む文字列
        interval: int, default: 0
            同じ画面の書き込みフレーム数
        add_text: bool, default: True
            表示後のテキストに追加するか否か
        """
        display_text = self.displayed_text + text
        if add_text:
            self.displayed_text += text
        
        bg = self.bg.copy()
        draw = ImageDraw.Draw(bg)
        lt_x, lt_y, rb_x, rb_y = draw.textbbox(
            (0, 0), display_text, 
            font=self.font, 
            anchor="la", spacing=self.spacing, 
        )
        display_height = abs(lt_y - rb_y)
        if display_height < self.height:
            draw.text(
                (0, 0), display_text, 
                fill=self.font_color, font=self.font, 
                anchor="la", spacing=self.spacing, 
            )
        else:
            draw.text(
                (0, self.height), display_text, 
                fill=self.font_color, font=self.font, 
                anchor="ld", spacing=self.spacing, 
            )
        img = pil2cv(bg)
        if interval != 0:
            pbar = tqdm(range(int(interval)), leave=False, desc="interval")
            for _ in pbar: 
                self.video.write(img)
        else:
            self.video.write(img)
    
    def create(self,):
        """
        ブート画面動画の作成
        """
        self.displayed_text = ""
        for cfg, txt in zip(tqdm(self.boot_cfg, desc="Process", ascii=True), self.boot_txt):
            dc = DisplayConfig(config=cfg)
            
            if dc.loading_type is not None:
                loading_text = self.loading_text[dc.loading_type]
                loading_text_n = len(loading_text)
                
                loop_cycle = int(dc.loading_time / dc.loading_interval)
                if dc.loading_unit == SEC:
                    if dc.loading_interval != 0:
                        loop_interval = self.fps * dc.loading_interval
                    else:
                        loop_interval = self.interval_sec
                elif dc.loading_unit == FRAME:
                    if dc.loading_interval != 0:
                        loop_interval = int(dc.loading_interval)
                    else:
                        loop_interval = self.interval_frame
                pbar = tqdm(range(loop_cycle), leave=False, desc="Loading")
                for i in pbar:
                    lt_n = i % loading_text_n
                    self._draw_text(
                        text=loading_text[lt_n], interval=loop_interval, 
                        add_text=False
                    )
            
            if dc.show_type == MOMENT:
                self._draw_text(text=txt)
            elif dc.show_type == GRADUALLY:
                txt_n = len(txt)
                loop_cycle = int(dc.show_time / dc.show_interval)
                if dc.show_unit == SEC:
                    if dc.show_interval != 0:
                        loop_interval = self.fps * dc.show_interval
                    else:
                        loop_interval = self.fps * self.interval_sec
                elif dc.show_unit == FRAME:
                    if dc.show_interval != 0:
                        loop_interval = dc.show_interval
                    else:
                        loop_interval = self.interval_frame
                pbar = tqdm(range(loop_cycle-1), leave=False, desc="GRADUALLY")
                for i in pbar:
                    bt_n = int(txt_n / loop_cycle * i)
                    self._draw_text(
                        text=txt[:bt_n], interval=loop_interval, add_text=False
                    )
                else:
                    self._draw_text(text=txt, interval=loop_interval)
            elif dc.show_type == L_BY_L:
                txt_splitlines = txt.splitlines()
                loop_cycle = len(txt_splitlines)
                if dc.show_time != 0:
                    if dc.show_unit == SEC:
                        loop_interval = self.fps * dc.show_time / loop_cycle
                    elif dc.show_unit == FRAME:
                        loop_interval = dc.show_time / loop_cycle
                elif dc.show_interval != 0:
                    if dc.show_unit == SEC:
                        loop_interval = self.fps * dc.show_interval
                    elif dc.show_unit == FRAME:
                        loop_interval = dc.show_interval
                else:
                    if dc.show_unit == SEC:
                        loop_interval = self.fps * self.interval_sec
                    elif dc.show_unit == FRAME:
                        loop_interval = self.interval_frame
                pbar = tqdm(range(loop_cycle-1), leave=False, desc="L_BY_L")
                for i in pbar:
                    t = "".join(txt_splitlines[:i])
                    self._draw_text(
                        text=t, interval=loop_interval, add_text=False
                    )
                else:
                    self._draw_text(text=txt, interval=loop_interval)
            elif dc.show_type == F_BY_F:
                loop_cycle = len(txt)
                pbar = tqdm(range(loop_cycle-1), leave=False, desc="F_BY_F")
                for i in pbar:
                    t = "".join(txt[:i])
                    self._draw_text(text=t, add_text=False)
                else:
                    self._draw_text(text=txt)
    
    def output(self,):
        """
        ブート画面動画の出力・圧縮
        動画圧縮: https://syobochim.hatenablog.com/entry/2021/01/07/004600
        """
        self.create()
        self.video.release()
        # 圧縮
        """
        root, ext = os.path.splitext(self.output_path)
        min_path = f"{root}-min{ext}"
        subprocess.call(f"ffmpeg -i {self.output_path} -crf {self.crf} {min_path}", shell=True)
        os.remove(self.output_path)
        """
        root, ext = os.path.splitext(self.output_path)
        min_path = f"{root}-min{ext}"
        stream = ffmpeg.input(self.output_path)
        stream = ffmpeg.output(stream, min_path, crf=self.crf)
        ffmpeg.run(stream)
        os.remove(self.output_path)
        print(f"Output: {os.path.abspath(min_path)}")