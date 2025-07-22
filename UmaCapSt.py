import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import win32gui
import os
import json
import datetime
from pathlib import Path
import subprocess
import mss
from screeninfo import get_monitors
import win32gui
import win32con
import time

CONFIG_FILE = 'config.json'
DEFAULT_DIR = os.path.join(os.getcwd(), "Screenshots")

os.makedirs(DEFAULT_DIR, exist_ok=True)

def find_umamusume_window(title):
    def handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            result.append(hwnd)
    found = []
    win32gui.EnumWindows(handler, found)
    return found[0] if found else None

def get_client_rect(hwnd):
    cl, ct = win32gui.ClientToScreen(hwnd, (0, 0))
    client_w, client_h = win32gui.GetClientRect(hwnd)[2:]
    return (cl, ct, cl + client_w, ct + client_h)

def get_monitor_index(x, y):
    for i, m in enumerate(get_monitors()):
        if m.x <= x < m.x + m.width and m.y <= y < m.y + m.height:
            return i + 1  # mss uses 1-based index
    return 1  # fallback

def load_config():
    default_cfg = {
        "save_dir": DEFAULT_DIR,
        "app_width": 100,
        "app_height": 400,
        "app_shift_x": 10,
        "app_shift_y": 300,
        "left_crop_ratio": 0.08,
        "right_crop_ratio": 0.09,
        "capture_delay": 0.1
    }

    if not os.path.exists(CONFIG_FILE):
        return default_cfg

    try:
        with open(CONFIG_FILE, 'r') as f:
            user_cfg = json.load(f)
            for key in default_cfg:
                if key not in user_cfg or not isinstance(user_cfg[key], (int, float, str)):
                    user_cfg[key] = default_cfg[key]
            return user_cfg
    except:
        return default_cfg

def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f)

class UmaCapStApp:
    def __init__(self, root):
        self.config = load_config()
        self.save_dir = self.config["save_dir"]
        self.game_title = self.config.get("game_title", "UmamusumePrettyDerby_Jpn")
        self.app_width = self.config.get("app_width", 100)
        self.app_height = self.config.get("app_height", 400)
        self.app_shift_x = self.config.get("app_shift_x", 10)
        self.app_shift_y = self.config.get("app_shift_y", 300)

        self.root = root
        self.root.title("UmaCapSt")
        self.root.geometry(f"{self.app_width}x{self.app_height}")
        self.root.resizable(False, False)

        hwnd = find_umamusume_window(self.game_title)
        if hwnd:
            x, y, _, _ = win32gui.GetWindowRect(hwnd)
            self.root.geometry(f"+{x + self.app_shift_x}+{y + self.app_shift_y}")

        self.topmost = True
        self.root.attributes('-topmost', self.topmost)

        self.button_frame = tk.Frame(root, width=self.app_width)
        self.button_frame.pack(side=tk.TOP, pady=10)

        # 保存指定／保存開く
        btn_select = tk.Button(self.button_frame, text="SetFolder", command=self.select_folder, width=14)
        btn_select.pack(pady=5, padx=5)
        btn_open = tk.Button(self.button_frame, text="OpenFolder", command=self.open_folder, width=14)
        btn_open.pack(pady=5, padx=5)

        # PNGアイコン付きボタン（全体、左、右）
        actions = [
            ("FullScreen", lambda: self.capture("full")),
            ("LeftHalf", lambda: self.capture("left")),
            ("RightHalf", lambda: self.capture("right"))
        ]
        for i, (_, cmd) in enumerate(actions):
            try:
                img = Image.open(f"img/btn{i}.png")
                visible_width = self.app_width - 10
                scale = visible_width / img.width
                resized = img.resize((visible_width, int(img.height * scale)), Image.LANCZOS)
                tkimg = ImageTk.PhotoImage(resized)
            except:
                tkimg = None
            btn = tk.Button(self.button_frame, image=tkimg, command=cmd)
            btn.image = tkimg
            btn.pack(pady=5, padx=5)

        self.toggle_button = tk.Button(root, text="TOP ON", command=self.toggle_topmost, width=14)
        self.toggle_button.pack(pady=5, padx=5)

        self.thumbnail_label = tk.Label(root)
        self.thumbnail_label.pack(side=tk.BOTTOM, pady=10)

    def toggle_topmost(self):
        self.topmost = not self.topmost
        self.root.attributes('-topmost', self.topmost)
        self.toggle_button.config(text="TOP ON" if self.topmost else "TOP OFF")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_dir = folder
            self.config["save_dir"] = folder
            save_config(self.config)

    def open_folder(self):
        if os.path.isdir(self.save_dir):
            path = Path(self.save_dir).resolve()
            subprocess.Popen(["explorer", str(path)])

    def capture(self, mode):
        hwnd = find_umamusume_window(self.game_title)
        if not hwnd:
            self.thumbnail_label.config(text="Game Window not found", image=None)
            return
        
        # ← ここでウマ娘ウィンドウを最前面に持ってくる！
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        # キャプチャタイミングをディレイ
        time.sleep(self.config.get("capture_delay", 0.1))

        # ウィンドウのクライアント領域を取得
        cl, ct, cr, cb = get_client_rect(hwnd)
        total_w = cr - cl
        total_h = cb - ct
        half_w = total_w // 2

        monitor_index = get_monitor_index(cl, ct)

        with mss.mss() as sct:
            if mode == "full":
                region = {"left": cl, "top": ct, "width": total_w, "height": total_h, "mon": monitor_index}
                sct_img = sct.grab(region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

            elif mode == "left":
                half_w = half_w - 2
                region = {"left": cl, "top": ct, "width": half_w, "height": total_h, "mon": monitor_index}
                sct_img = sct.grab(region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                cut_px = int(total_w * self.config.get("left_crop_ratio", 0.08))
                img = img.crop((cut_px, 0, img.width, img.height))

            elif mode == "right":
                region = {"left": cl + half_w, "top": ct, "width": half_w, "height": total_h, "mon": monitor_index}
                sct_img = sct.grab(region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                cut_px = int(total_w * self.config.get("right_crop_ratio", 0.09))
                img = img.crop((0, 0, img.width - cut_px, img.height))

            else:
                return

        filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(self.save_dir, filename)
        img.save(path)

        visible_width = self.app_width - 10
        scale = visible_width / img.width
        thumb = img.resize((visible_width, int(img.height * scale)), Image.LANCZOS)
        tkthumb = ImageTk.PhotoImage(thumb)
        
        self.thumbnail_label.config(text="")
        self.thumbnail_label.config(image=tkthumb, text="")
        self.thumbnail_label.image = tkthumb

if __name__ == "__main__":
    root = tk.Tk()
    app = UmaCapStApp(root)
    root.mainloop()