
LOADING = "loading" # ローディング
SHOW = "show"
TEXT = "text" # ブート文字の表示
TYPE = "type" # ローディング/ブート文字表示のタイプ
MOMENT = "moment" # 瞬時：ブート文字表示タイプ
GRADUALLY = "gradually" # 徐々：ブート文字表示タイプ
L_BY_L = "line_by_line" # 行ごとに文字表示：ブート文字表示タイプ
F_BY_F = "frame_by_frame" # フレームごとに一文字ずつ表示：ブート文字表示タイプ
NONE = None
TIME = "time"
INTERVAL = "interval"
UNIT = "unit"
SEC = "sec"
FRAME = "frame"

class DisplayConfig():
    """
    boot_text.txt のブートテキストの設定
    
    Attributes
    ----------
    loading: dict
        ローディングテキストの設定
    boot: dict
        ブートテキストの設定
    .type: str
        loading, boot の表示タイプ
    .time: float
        文字表示完了までの時間
    .interval: float
        文字表示までのインターバルの時間
    .unit: str, "frame" or "sec"
        .time .interval の単位
    """
    def __init__(self, config: dict) -> None:
        """
        loading.type = cfg[LOADING][TYPE]
        loading.time = cfg[LOADING][TIME]
        loading.interval = cfg[LOADING][INTERVAL]
        loading.unit = cfg[LOADING][UNIT]
        show.type = cfg[SHOW][TYPE]
        show.time = cfg[SHOW][TIME]
        show.time = cfg[SHOW][INTERVAL]
        show.unit = cfg[SHOW][UNIT]
        """
        for k, v in config.items():
            if type(v) is not dict:
                setattr(self, k.lower(), v)
            else:
                for kk, vv in v.items():
                    setattr(self, f"{k.lower()}_{kk.lower()}", vv)