# 导入所需模块
import tkinter as tk  # GUI库
from tkinter import filedialog, messagebox  # 文件对话框和消息框
import pysrt  # 用于处理SRT字幕的库

# 定义SRTtoLRCConverter类
class SRTtoLRCConverter:
    def __init__(self, master):
        # 初始化主窗口
        self.master = master
        self.master.title("SRT 到 LRC 转换器")
        self.master.configure(bg="#E6E6FA")  # 设置主窗口背景色

        # 初始化变量
        self.srt_file_path = ""  # SRT文件路径
        self.lrc_file_path = ""  # LRC文件路径

        # 创建文本框和标签
        self.srt_textbox = tk.Text(self.master, wrap="word", width=50, height=10, bg="#BEBEBE")  # 设置SRT文本框背景色
        self.srt_textbox.grid(row=0, column=0, columnspan=2)

        self.lrc_textbox = tk.Text(self.master, wrap="word", width=50, height=10, bg="#BEBEBE")  # 设置LRC文本框背景色
        self.lrc_textbox.grid(row=1, column=0, columnspan=2)

        # 创建按钮
        self.open_srt_button = tk.Button(self.master, text="打开SRT文件", command=self.open_srt)  # 打开SRT文件按钮
        self.open_srt_button.grid(row=2, column=0)

        self.convert_button = tk.Button(self.master, text="转换", command=self.convert)  # 转换按钮
        self.convert_button.grid(row=2, column=1)

        self.save_lrc_button = tk.Button(self.master, text="保存LRC文件", command=self.save_lrc)  # 保存LRC文件按钮
        self.save_lrc_button.grid(row=3, column=0)

        self.save_lrc_entry = tk.Entry(self.master, width=50, bg="#CDC1C5")  # 设置保存路径输入框背景色
        self.save_lrc_entry.grid(row=3, column=1)

    # 打开SRT文件方法
    def open_srt(self):
        # 使用文件对话框打开SRT文件
        self.srt_file_path = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])

        # 如果选择了文件，读取内容并显示在SRT文本框中
        if self.srt_file_path:
            with open(self.srt_file_path, "r", encoding="utf-8") as f:
                srt_content = f.read()
                self.srt_textbox.insert("1.0", srt_content)

    # 转换方法
    def convert(self):
        # 检查SRT文件是否已打开
        if not self.srt_file_path:
            messagebox.showerror("Error", "请先打开一个SRT文件。")
            return

        # 读取SRT文件内容
        subs = pysrt.open(self.srt_file_path)
        lrc_content = ""

        # 遍历SRT字幕，转换为LRC格式
        for sub in subs:
            # 将时间对象转换为字符串，并按照冒号分割
            time_str = sub.start.to_time().strftime('%H:%M:%S,%f')[:-3]
            hh_mm_ss_ms = time_str.split(':')
            hh, mm, ss, ms = int(hh_mm_ss_ms[0]), int(hh_mm_ss_ms[1]), int(hh_mm_ss_ms[2].split(',')[0]), int(hh_mm_ss_ms[2].split(',')[1])

            # 根据进制累加小时到分钟
            mm += hh * 60

            # 保留三位毫秒
            ms = f"{ms:03d}"

            # 构建LRC时间格式
            lrc_time = f"{mm:02d}:{ss:02d}.{ms}"

            # 添加到LRC内容
            lrc_content += f"[{lrc_time}]{sub.text}\n"

        # 清空LRC文本框并插入转换后的内容
        self.lrc_textbox.delete("1.0", tk.END)
        self.lrc_textbox.insert("1.0", lrc_content)

    # 保存LRC文件方法
    def save_lrc(self):
        # 使用文件对话框保存LRC文件
        if not self.lrc_file_path:
            self.lrc_file_path = filedialog.asksaveasfilename(
                defaultextension=".lrc",
                filetypes=[("LRC Files", "*.lrc")],
                initialfile="output.lrc",
                initialdir=".",
            )

        # 如果选择了保存路径，更新输入框并保存内容
        if self.lrc_file_path:
            self.save_lrc_entry.delete(0, tk.END)
            self.save_lrc_entry.insert(0, self.lrc_file_path)
            with open(self.lrc_file_path, "w", encoding="utf-8") as f:
                f.write(self.lrc_textbox.get("1.0", tk.END))

# 创建Tkinter主窗口
root = tk.Tk()

# 实例化SRTtoLRCConverter类
app = SRTtoLRCConverter(root)

# 开始主循环
root.mainloop()