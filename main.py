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
        self.geometry("900x700")
        self.minsize(900, 700)

        # 现代感主题配置
        self.current_mode = "Dark"
        ct.set_appearance_mode(self.current_mode)
        ct.set_default_color_theme("blue")

        # 加载自定义字体
        self.custom_font = font.Font(family="Microsoft YaHei", size=14)

        # 初始化数据管理器
        self.manager = SentenceManager()

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        """构建GUI组件"""
        # 主容器
        self.main_frame = ct.CTkFrame(
            self,
            corner_radius=20,
            border_width=0,
            fg_color=("white", "#1a1a1a")
        )
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 模式切换按钮
        self.mode_btn = ct.CTkButton(
            self.main_frame,
            text="Light" if self.current_mode == "Dark" else "Dark",
            command=self.toggle_mode,
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=("#F0F0F0", "#333333")
        )
        self.mode_btn.place(relx=0.95, rely=0.05, anchor="center")

        # 标题标签
        self.title_label = ct.CTkLabel(
            self.main_frame,
            text="答案之书",
            font=("Microsoft YaHei", 32, "bold"),
            text_color=("#FF6B6B", "#FFD700"),
            pady=20
        )
        self.title_label.pack(pady=(20, 10))

        # 使用说明
        self.instructions = ct.CTkLabel(
            self.main_frame,
            text="人人都有困惑迷茫的时候，这个程序可以作为您的参考。\n请您闭上双眼，默念自己的问题30秒，清空大脑，\n然后输入问题，点击下面的按钮获取启示",
            font=("Microsoft YaHei", 16),
            text_color=("#666666", "#A0A0A0"),
            wraplength=600,
            justify="center"
        )
        self.instructions.pack(pady=20)

        # 问题输入框
        self.question_entry = ct.CTkEntry(
            self.main_frame,
            placeholder_text="在这里写下您的问题...",
            font=("Microsoft YaHei", 16),
            width=500,
            height=40,
            corner_radius=12,
            border_color=("#808080", "#404040"),
            fg_color=("white", "#2B2B2B"),
            text_color=("black", "white")
        )
        self.question_entry.pack(pady=15)

        # 句子显示框
        self.sentence_display = ct.CTkTextbox(
            self.main_frame,
            width=550,
            height=200,
            font=("Microsoft YaHei", 20, "italic"),
            wrap="word",
            fg_color=("#F8F9FA", "#2B2B2B"),
            border_width=2,
            corner_radius=15,
            border_color=("#DEE2E6", "#404040"),
            scrollbar_button_color=("#6C757D", "#495057"),
            scrollbar_button_hover_color=("#ADB5BD", "#343A40")
        )
        self.sentence_display.pack(pady=20, padx=20, fill="both")
        self.sentence_display.insert("end", "等待你的答案...")
        self.sentence_display.configure(state="disabled")

        # 加载动画
        self.loading_label = ct.CTkLabel(
            self.main_frame,
            text="",
            font=("Microsoft YaHei", 18),
            text_color=("#6C757D", "#ADB5BD")
        )

        # 操作按钮（修复布局问题）
        button_frame = ct.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x", padx=50)  # 增加填充和边距

        # 使用grid布局确保按钮正确排列
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.random_btn = ct.CTkButton(
            button_frame,
            text="✨ 获取启示 ✨",
            command=self.show_random_sentence,
            width=180,
            height=50,
            font=("Microsoft YaHei", 18, "bold"),
            corner_radius=12,
            border_width=2,
            border_color=("#FF6B6B", "#FFD700"),
            fg_color=("#4ECDC4", "#2FA572"),
            hover_color=("#45B7B0", "#1E7049"),
            text_color="white"
        )
        self.random_btn.grid(row=0, column=0, padx=10)

        quit_btn = ct.CTkButton(
            button_frame,
            text="退出程序",
            command=self.destroy,
            width=120,
            height=40,
            fg_color=("#FF6B6B", "#FF4B4B"),
            hover_color=("#FF8787", "#D14343"),
            font=("Microsoft YaHei", 14),
            corner_radius=8
        )
        quit_btn.grid(row=0, column=1, padx=10)

    def toggle_mode(self):
        """切换日间/夜间模式"""
        self.current_mode = "Light" if self.current_mode == "Dark" else "Dark"
        ct.set_appearance_mode(self.current_mode)
        self.mode_btn.configure(text="Dark" if self.current_mode == "Light" else "Light")

        # 更新组件颜色
        color_set = {
            "title": ("#FF6B6B", "#FFD700"),
            "border": ("#DEE2E6", "#404040"),
            "button_border": ("#FF6B6B", "#FFD700"),
            "button_fg": ("#4ECDC4", "#2FA572")
        }

        self.title_label.configure(text_color=color_set["title"])
        self.sentence_display.configure(border_color=color_set["border"])
        self.random_btn.configure(
            border_color=color_set["button_border"],
            fg_color=color_set["button_fg"]
        )

    def show_loading_animation(self):
        """显示加载动画"""
        self.loading_label.pack()
        dots = ["   ", ".  ", ".. ", "..."]
        for i in range(12):
            self.loading_label.configure(text="宇宙正在思考" + dots[i % 4])
            self.update()
            time.sleep(0.2)
        self.loading_label.pack_forget()

    def show_random_sentence(self):
        """显示随机句子的动画效果"""
        # 检查问题输入
        if len(self.question_entry.get().strip()) == 0:
            messagebox.showwarning("提示", "人家还不知道您的问题喵！")
            self.question_entry.focus()
            return

        # 禁用按钮防止重复点击
        self.random_btn.configure(state="disabled")

        # 显示加载动画
        self.show_loading_animation()

        # 清空显示区域
        self.sentence_display.configure(state="normal")
        self.sentence_display.delete("1.0", "end")

        # 获取数据
        page, text = self.manager.get_random_sentence()

        # 修复颜色配置问题
        current_color = "#6C757D" if self.current_mode == "Light" else "#ADB5BD"
        self.sentence_display.tag_config("fade", foreground=current_color)

        # 逐字显示动画
        full_text = f"{page}\n\n{text}"
        for i in range(len(full_text) + 1):
            partial_text = full_text[:i]
            self.sentence_display.delete("1.0", "end")
            self.sentence_display.insert("end", partial_text, "fade")
            self.update()
            time.sleep(0.03)

        # 最终效果
        self.sentence_display.tag_remove("fade", "1.0", "end")
        self.sentence_display.configure(text_color=("#212529", "#F8F9FA"))
        self.random_btn.configure(state="normal")


# ====================
# 运行程序
# ====================
if __name__ == "__main__":
    app = App()
    app.mainloop()