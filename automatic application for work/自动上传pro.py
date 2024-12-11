import cv2
import numpy as np
import pyautogui
import time
from PIL import Image, ImageGrab, ImageTk
import os
import win32gui
import win32con
import ctypes
import tkinter as tk
from tkinter import ttk
import sys

class InfoWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("程序信息 / Program Information")
        
        # 设置更大的窗口
        window_width = 800
        window_height = 600  # 增加高度以容纳新按钮
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 作者信息标签
        author_label = ttk.Label(
            self.root, 
            text="程序作者 / Program Author: Mai Jiaming",
            font=("Arial", 14)
        )
        author_label.pack(pady=30)
        
        # 打赏按钮
        donate_button = ttk.Button(
            self.root,
            text="打赏作者 / Donate",
            command=self.show_donate_window,
            width=40
        )
        donate_button.pack(pady=20)
        
        # 跳过按钮
        skip_button = ttk.Button(
            self.root,
            text="跳过打赏 / Skip",
            command=self.close_window,
            width=40
        )
        skip_button.pack(pady=20)
        
        # 笔记本提示文本
        laptop_label = ttk.Label(
            self.root,
            text="如果你使用的不是外接屏幕而是仅使用笔记本电脑的屏幕运行，请先按照提示设置：\nIf you are using laptop screen instead of external monitor, please follow the setup guide:",
            font=("Arial", 12),
            wraplength=550
        )
        laptop_label.pack(pady=10)
        
        # 笔记本设置提示按钮
        laptop_tip_button = ttk.Button(
            self.root,
            text="笔记本电脑设置提示 / Laptop Setup Guide",
            command=self.show_laptop_tip,
            width=40
        )
        laptop_tip_button.pack(pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        
    def show_donate_window(self):
        """显示打赏窗口"""
        donate_window = tk.Toplevel(self.root)
        donate_window.title("打赏作者 / Donate")
        
        # 设置更大的打赏窗口，考虑图片比例
        window_width = 600
        window_height = 900
        screen_width = donate_window.winfo_screenwidth()
        screen_height = donate_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        donate_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 加载收款码图片
        if getattr(sys, 'frozen', False):
            image_path = os.path.join(sys._MEIPASS, "截图", "收款码.png")
        else:
            image_path = r"C:\脚本\截图\收款码.png"
            
        if os.path.exists(image_path):
            img = Image.open(image_path)
            # 保持原始比例缩放
            original_width, original_height = img.size
            target_width = 400
            target_height = int(target_width * original_height / original_width)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # 显示图片
            label = tk.Label(donate_window, image=photo)
            label.image = photo
            label.pack(pady=30)
        else:
            print(f"警告: 找不到收款码图片: {image_path}")
        
        # 关闭按钮
        close_button = ttk.Button(
            donate_window,
            text="关闭 / Close",
            command=lambda: self.close_donate_window(donate_window),
            width=40
        )
        close_button.pack(pady=30)
        
        # 等待窗口关闭
        self.root.wait_window(donate_window)
        # 关闭主窗口
        self.close_window()
        
    def show_laptop_tip(self):
        """显示笔记本设置提示窗口"""
        tip_window = tk.Toplevel(self.root)
        tip_window.title("笔记本设置提示 / Laptop Setup Guide")
        
        # 设置窗口大小和位置
        window_width = 1200
        window_height = 900
        screen_width = tip_window.winfo_screenwidth()
        screen_height = tip_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        tip_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 加载提示图片
        if getattr(sys, 'frozen', False):
            image_path = os.path.join(sys._MEIPASS, "截图", "提示.png")
        else:
            image_path = r"C:\脚本\截图\提示.png"
            
        if os.path.exists(image_path):
            img = Image.open(image_path)
            # 调整图片大小以适应窗口
            img = img.resize((1100, 800), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # 显示图片
            label = tk.Label(tip_window, image=photo)
            label.image = photo
            label.pack(pady=30)
        else:
            print(f"警告: 找不到提示图片: {image_path}")        
               
    def close_donate_window(self, window):
        """关闭打赏窗口"""
        window.destroy()
        
    def close_window(self):
        """关闭主窗口"""
        self.root.destroy()
        
    def show(self):
        self.root.mainloop()
class AutoClicker:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        # 设置命令行窗口位置
        self.set_window_position()
        
        # 获取程序运行目录
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, "截图")
        else:
            base_path = r"C:\脚本\截图"
        
        # 设置所有按钮的多个图片路径
        self.button1_paths = [
            os.path.join(base_path, "actions.png"),
            os.path.join(base_path, "actions2.png"),
            os.path.join(base_path, "actions3.png"),
            os.path.join(base_path, "actions4.png")
        ]
        
        self.button2_paths = [
            os.path.join(base_path, "bt2.png"),
            os.path.join(base_path, "bt2_2.png"),
            os.path.join(base_path, "bt2_3.png"),
            os.path.join(base_path, "bt2_4.png")
        ]
        
        self.ok_paths = [
            os.path.join(base_path, "OK.png"),
            os.path.join(base_path, "OK2.png"),
            os.path.join(base_path, "OK3.png"),
            os.path.join(base_path, "OK4.png")
        ]
        
        self.xml_paths = [
            os.path.join(base_path, "dsw.png"),
            os.path.join(base_path, "dsw2.png")
        ]
        
        # 加载所有按钮的模板
        self.button1_templates = []
        for path in self.button1_paths:
            if os.path.exists(path):
                pil_image = Image.open(path)
                template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                self.button1_templates.append(template)
            else:
                print(f"警告: 找不到图片: {path}")
                
        # 加载所有按钮2的模板
        self.button2_templates = []
        for path in self.button2_paths:
            if os.path.exists(path):
                pil_image = Image.open(path)
                template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                self.button2_templates.append(template)
            else:
                print(f"警告: 找不到图片: {path}")
                
        # 加载所有OK按钮的模板
        self.ok_templates = []
        for path in self.ok_paths:
            if os.path.exists(path):
                pil_image = Image.open(path)
                template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                self.ok_templates.append(template)
            else:
                print(f"警告: 找不到图片: {path}")
                
        # 加载所有XML位置图片
        self.xml_templates = []
        for path in self.xml_paths:
            if os.path.exists(path):
                pil_image = Image.open(path)
                template = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                self.xml_templates.append(template)
            else:
                print(f"警告: 找不到图片: {path}")
            
        print("所有图片加载成功")
    def set_window_position(self):
        """设置命令行窗口位置和大小"""
        try:
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            hwnd = win32gui.GetForegroundWindow()
            window_width = screen_width // 5
            window_height = screen_height // 2
            x_position = 1
            y_position = screen_height - window_height
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x_position, y_position, 
                                window_width, window_height, win32con.SWP_SHOWWINDOW)
        except Exception as e:
            print(f"设置窗口位置时出错: {str(e)}")

    def check_folder_empty(self, folder_path=r"C:\脚本\xml文件"):
        """检查文件夹是否为空"""
        try:
            if not os.path.exists(folder_path):
                print(f"文件夹不存在: {folder_path}")
                return False
            files = os.listdir(folder_path)
            is_empty = len(files) == 0
            if is_empty:
                print("文件夹为空")
            else:
                print(f"文件夹中有 {len(files)} 个文件")
            return is_empty
        except Exception as e:
            print(f"检查文件夹时出错: {str(e)}")
            return False

    def delete_oldest_file(self, folder_path=r"C:\脚本\xml文件"):
        """删除指定文件夹中最旧的文件"""
        try:
            if not os.path.exists(folder_path):
                print(f"文件夹不存在: {folder_path}")
                return False
            files = sorted(
                (os.path.join(folder_path, f) for f in os.listdir(folder_path)),
                key=os.path.getmtime
            )
            if files:
                os.remove(files[0])
                print(f"已删除文件: {files[0]}")
                return True
            print("没有可删除的文件")
            return False
        except Exception as e:
            print(f"删除文件时出错: {str(e)}")
            return False

    def find_button_with_templates(self, templates, button_name, threshold=0.7):
        """使用多个模板查找按钮"""
        try:
            print(f"\n开始查找{button_name}...")
            screen = np.array(ImageGrab.grab())
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            
            best_match = None
            best_score = threshold
            best_location = None
            
            for template in templates:
                if screen.shape[2] != template.shape[2]:
                    template = cv2.cvtColor(template, cv2.COLOR_GRAY2BGR)
                
                screen_copy = screen.astype(np.uint8)
                template = template.astype(np.uint8)
                
                result = cv2.matchTemplate(screen_copy, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_score:
                    best_score = max_val
                    best_location = max_loc
                    best_match = template
            
            if best_match is not None:
                h, w = best_match.shape[:2]
                center_x = best_location[0] + w//2
                center_y = best_location[1] + h//2
                
                print(f"找到{button_name}，最佳匹配度: {best_score:.2f}")
                print(f"位置: ({center_x}, {center_y})")
                
                if button_name == "按钮2" or button_name == "OK按钮":
                    pyautogui.moveTo(center_x, center_y, duration=0.1)
                    time.sleep(0.05)
                else:
                    pyautogui.moveTo(center_x, center_y, duration=0.2)
                    time.sleep(0.1)
                    
                pyautogui.click()
                print(f"已点击{button_name}")
                return True
            else:
                print(f"未找到{button_name} (最高匹配度: {best_score:.2f})")
                return False
                
        except Exception as e:
            print(f"操作出错: {str(e)}")
            print("错误详情:", type(e).__name__)
            import traceback
            traceback.print_exc()
            return False

    def find_and_click_first_file(self, threshold=0.6):
        """查找XML File位置并点击下半部分"""
        try:
            print("\n等待文件选择窗口出现...")
            time.sleep(0.5)
            
            screen = np.array(ImageGrab.grab())
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            
            best_match = None
            best_score = threshold
            best_location = None
            best_template = None
            
            for template in self.xml_templates:
                result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_score:
                    best_score = max_val
                    best_location = max_loc
                    best_template = template
            
            if best_template is not None:
                print(f"找到XML File位置，匹配度: {best_score:.2f}")
                h, w = best_template.shape[:2]
                center_x = best_location[0] + w//2
                center_y = best_location[1] + int(h * 0.75)
                
                pyautogui.moveTo(center_x, center_y, duration=0.1)
                time.sleep(0.05)
                pyautogui.doubleClick()
                print("已双击XML File下半部分")
                return True
                
            print("未找到XML File位置")
            return False
                
        except Exception as e:
            print(f"处理文件选择时出错: {str(e)}")
            return False
    def click_buttons_in_sequence(self, max_attempts=3, retry_interval=1):
        """按顺序点击所有按钮"""
        # 首先检查文件夹是否为空
        if self.check_folder_empty():
            print("\n文件夹为空，任务完成")
            return "empty"
            
        # 首先点击按钮1
        for attempt in range(max_attempts):
            print(f"\n尝试点击按钮1 - 第 {attempt + 1}/{max_attempts} 次")
            if self.find_button_with_templates(self.button1_templates, "按钮1"):
                time.sleep(0.2)  # 按钮1到按钮2等待0.2秒
                for attempt2 in range(max_attempts):
                    if self.find_button_with_templates(self.button2_templates, "按钮2"):
                        print("按钮2点击成功")
                        print("等待0.2秒...")
                        time.sleep(0.2)  # 按钮2到xml file等待0.2秒
                        
                        print("检查文件夹是否为空...")
                        if self.check_folder_empty():
                            print("\n文件夹为空，任务完成")
                            return "empty"
                        
                        print("继续处理文件选择窗口...")
                        for attempt3 in range(max_attempts):
                            if self.find_and_click_first_file():
                                print("成功处理文件选择窗口")
                                
                                print("等待8秒...")
                                time.sleep(8)
                                # 一直尝试点击OK按钮直到成功
                                while True:
                                    if self.find_button_with_templates(self.ok_templates, "OK按钮"):
                                        print("成功点击OK按钮")
                                        print("等待1秒...")
                                        time.sleep(1)
                                        print("\n开始删除旧文件...")
                                        self.delete_oldest_file()
                                        return True
                                    print(f"等待 {retry_interval} 秒后重试点击OK按钮...")
                                    time.sleep(retry_interval)
                            
                            if attempt3 < max_attempts - 1:
                                print(f"等待 {retry_interval} 秒后重试处理文件选择窗口...")
                                time.sleep(retry_interval)
                        
                    if attempt2 < max_attempts - 1:
                        print(f"等待 {retry_interval} 秒后重试按钮2...")
                        time.sleep(retry_interval)
                return False
            
            if attempt < max_attempts - 1:
                print(f"等待 {retry_interval} 秒后重试按钮1...")
                time.sleep(retry_interval)
        
        print("未能完成所有操作")
        return False

def main():
    try:
        # 显示信息窗口
        info_window = InfoWindow()
        info_window.show()
        
        print("自动点击程序启动...")
        print("注意: 移动鼠标到屏幕左上角可以紧急停止程序")
        
        clicker = AutoClicker()
        
        while True:
            result = clicker.click_buttons_in_sequence()
            
            if result == "empty":
                print("\n检测到文件夹为空")
                input("操作已完成，按Enter键退出...")
                break
            elif result:
                print("\n本轮操作完成，继续下一轮...")
                time.sleep(3)
            else:
                print("\n操作失败，继续重试...")
                time.sleep(3)
                
    except Exception as e:
        print(f"程序发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        input("按Enter键退出...")

if __name__ == "__main__":
    main()
