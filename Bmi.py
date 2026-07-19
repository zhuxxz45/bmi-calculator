import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI 计算器")
        self.root.geometry("360x420")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f4ff')
        
        # 标题
        title = tk.Label(root, text="📊 BMI 计算器", font=("Microsoft YaHei", 22, "bold"), bg='#f0f4ff', fg='#1a2a4a')
        title.pack(pady=(20, 15))
        
        # 性别
        gender_frame = tk.Frame(root, bg='#f0f4ff')
        gender_frame.pack(fill='x', padx=30, pady=5)
        tk.Label(gender_frame, text="性别", font=("Microsoft YaHei", 14, "bold"), bg='#f0f4ff', fg='#2a3a5a').pack(anchor='w')
        self.gender = ttk.Combobox(gender_frame, values=['男', '女'], font=("Microsoft YaHei", 14), state='readonly')
        self.gender.set('男')
        self.gender.pack(fill='x', pady=(3, 0))
        
        # 年龄
        age_frame = tk.Frame(root, bg='#f0f4ff')
        age_frame.pack(fill='x', padx=30, pady=5)
        tk.Label(age_frame, text="年龄", font=("Microsoft YaHei", 14, "bold"), bg='#f0f4ff', fg='#2a3a5a').pack(anchor='w')
        self.age = tk.Entry(age_frame, font=("Microsoft YaHei", 14), bg='#fafcff', relief='flat', highlightthickness=2, highlightcolor='#4a7aff', highlightbackground='#dce3ef')
        self.age.pack(fill='x', pady=(3, 0))
        
        # 身高体重一行
        hw_frame = tk.Frame(root, bg='#f0f4ff')
        hw_frame.pack(fill='x', padx=30, pady=5)
        
        height_frame = tk.Frame(hw_frame, bg='#f0f4ff')
        height_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        tk.Label(height_frame, text="身高 (cm)", font=("Microsoft YaHei", 14, "bold"), bg='#f0f4ff', fg='#2a3a5a').pack(anchor='w')
        self.height = tk.Entry(height_frame, font=("Microsoft YaHei", 14), bg='#fafcff', relief='flat', highlightthickness=2, highlightcolor='#4a7aff', highlightbackground='#dce3ef')
        self.height.pack(fill='x', pady=(3, 0))
        
        weight_frame = tk.Frame(hw_frame, bg='#f0f4ff')
        weight_frame.pack(side='right', fill='x', expand=True, padx=(5, 0))
        tk.Label(weight_frame, text="体重 (kg)", font=("Microsoft YaHei", 14, "bold"), bg='#f0f4ff', fg='#2a3a5a').pack(anchor='w')
        self.weight = tk.Entry(weight_frame, font=("Microsoft YaHei", 14), bg='#fafcff', relief='flat', highlightthickness=2, highlightcolor='#4a7aff', highlightbackground='#dce3ef')
        self.weight.pack(fill='x', pady=(3, 0))
        
        # 进度条
        self.progress_frame = tk.Frame(root, bg='#f0f4ff')
        self.progress_frame.pack(fill='x', padx=30, pady=(15, 0))
        self.progress = ttk.Progressbar(self.progress_frame, length=300, mode='determinate')
        self.progress.pack(fill='x')
        self.progress_label = tk.Label(self.progress_frame, text="", font=("Microsoft YaHei", 12), bg='#f0f4ff', fg='#4a6a9a')
        self.progress_label.pack()
        self.progress_frame.pack_forget()
        
        # 按钮
        self.btn = tk.Button(root, text="开始计算", font=("Microsoft YaHei", 17, "bold"), bg='#4a7aff', fg='white', relief='flat', cursor='hand2', command=self.calculate)
        self.btn.pack(fill='x', padx=30, pady=(15, 0), ipady=8)
        
        # 结果显示
        self.result = tk.Label(root, text="", font=("Microsoft YaHei", 18, "bold"), bg='#f0f4ff', fg='#1a2a4a')
        self.result.pack(pady=(15, 0))
    
    def calculate(self):
        gender = self.gender.get()
        age = self.age.get().strip()
        height = self.height.get().strip()
        weight = self.weight.get().strip()
        
        if not age or not height or not weight:
            messagebox.showerror("错误", "请完整填写所有字段")
            return
        
        try:
            age_val = int(age)
            height_val = float(height)
            weight_val = float(weight)
            
            if not (1 <= age_val <= 120 and 50 <= height_val <= 300 and 10 <= weight_val <= 300):
                messagebox.showerror("错误", "请输入有效范围：年龄1-120，身高50-300cm，体重10-300kg")
                return
            
            self.btn.config(state='disabled')
            self.result.config(text="")
            self.progress_frame.pack(fill='x', padx=30, pady=(15, 0))
            self.progress['value'] = 0
            self.progress_label.config(text="正在读取BMI...")
            
            def run():
                for i in range(0, 101, 5):
                    time.sleep(0.1)
                    self.progress['value'] = i
                    self.root.update()
                
                height_m = height_val / 100
                bmi = round(weight_val / (height_m * height_m), 2)
                
                self.root.after(0, lambda: self.show_result(bmi))
            
            threading.Thread(target=run, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")

    def show_result(self, bmi):
        self.progress_label.config(text="✅ 获取成功！")
        self.result.config(text=f"您的BMI是 {bmi}")
        messagebox.showinfo("BMI结果", f"您的BMI是 {bmi}")
        self.btn.config(state='normal')
        self.root.after(1500, lambda: self.progress_frame.pack_forget())

if __name__ == '__main__':
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()