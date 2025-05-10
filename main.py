import json
import random
import time
import customtkinter as ct
from tkinter import messagebox, font


# ====================
# 数据管理模块
# ====================
class SentenceManager:
    def __init__(self, filename="sentences.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """加载JSON数据，带有错误处理"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("错误", f"找不到数据文件 {self.filename}")
            exit()
        except json.JSONDecodeError:
            messagebox.showerror("错误", "数据文件格式不正确")
            exit()

    def get_random_sentence(self):
        """获取带页码的随机句子"""
        page, text = random.choice(list(self.data["pages"].items()))
        return f"第 {page} 页", text


# ====================
# GUI界面
# ====================
class App(ct.CTk):
    def __init__(self):
        super().__init__()

        # 初始化配置
        self.title("答案之书")
        self.geometry("800x600")
        self.minsize(700, 500)

        # 现代感主题配置
        ct.set_appearance_mode("Dark")
        ct.set_default_color_theme("dark-blue")

        # 加载自定义字体
        self.custom_font = font.Font(family="Microsoft YaHei", size=14)

        # 初始化数据管理器
        self.manager = SentenceManager()

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        """构建GUI组件"""
        # 主容器 - 添加渐变背景
        main_frame = ct.CTkFrame(
            self,
            corner_radius=20,
            border_width=0,
            fg_color=("white", "#1a1a1a"),  # 浅色/深色渐变
        )
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 标题标签
        self.title_label = ct.CTkLabel(
            main_frame,
            text="答案之书",
            font=("Microsoft YaHei", 32, "bold"),
            text_color="#FFD700",
            pady=20
        )
        self.title_label.pack(pady=(20, 10))

        # 使用说明
        self.instructions = ct.CTkLabel(
            main_frame,
            text="人人都有困惑迷茫的时候，这个程序可以作为你的参考。\n请你闭上双眼，默念自己的问题30秒，清空大脑，\n点击下面的按钮获取启示",
            font=("Microsoft YaHei", 16),
            text_color="#A0A0A0",
            wraplength=600,
            justify="center"
        )
        self.instructions.pack(pady=20)

        # 句子显示框 - 卡片式设计
        self.sentence_display = ct.CTkTextbox(
            main_frame,
            width=550,
            height=200,
            font=("Microsoft YaHei", 20, "italic"),
            wrap="word",
            fg_color="transparent",
            border_width=2,
            corner_radius=15,
            border_color="#404040",
            scrollbar_button_color="#606060",
            scrollbar_button_hover_color="#808080"
        )
        self.sentence_display.pack(pady=20, padx=20, fill="both")
        self.sentence_display.insert("end", "等待你的答案...")
        self.sentence_display.configure(state="disabled")

        # 加载动画
        self.loading_label = ct.CTkLabel(
            main_frame,
            text="",
            font=("Microsoft YaHei", 18),
            text_color="#808080"
        )

        # 操作按钮
        button_frame = ct.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.random_btn = ct.CTkButton(
            button_frame,
            text="✨ 获取启示 ✨",
            command=self.show_random_sentence,
            width=180,
            height=50,
            font=("Microsoft YaHei", 18, "bold"),
            corner_radius=12,
            border_width=2,
            border_color="#FFD700",
            fg_color="#2FA572",
            hover_color="#1E7049",
            text_color="white"
        )
        self.random_btn.pack(side="left", padx=20)

        # 退出按钮
        quit_btn = ct.CTkButton(
            button_frame,
            text="退出程序",
            command=self.destroy,
            width=120,
            height=40,
            fg_color="#FF4B4B",
            hover_color="#D14343",
            font=("Microsoft YaHei", 14),
            corner_radius=8
        )
        quit_btn.pack(side="right", padx=20)

    def show_loading_animation(self):
        """显示加载动画"""
        self.loading_label.pack()
        for i in range(3):
            self.loading_label.configure(text="思考中" + "." * (i + 1))
            self.update()
            time.sleep(0.5)
        self.loading_label.pack_forget()

    def show_random_sentence(self):
        """显示随机句子的动画效果"""
        # 禁用按钮防止重复点击
        self.random_btn.configure(state="disabled")

        # 显示加载动画
        self.show_loading_animation()

        # 清空显示区域
        self.sentence_display.configure(state="normal")
        self.sentence_display.delete("1.0", "end")

        # 获取数据
        page, text = self.manager.get_random_sentence()

        # 逐字显示动画
        self.sentence_display.tag_config("fade", foreground="#808080")
        for i in range(len(text) + 1):
            partial_text = text[:i]
            self.sentence_display.delete("1.0", "end")
            self.sentence_display.insert("end", partial_text, "fade")
            self.update()
            time.sleep(0.03)

        # 最终效果
        self.sentence_display.tag_remove("fade", "1.0", "end")
        self.sentence_display.configure(text_color="#FFFFFF")
        self.random_btn.configure(state="normal")


# ====================
# 运行程序
# ====================
if __name__ == "__main__":
    app = App()
    app.mainloop()