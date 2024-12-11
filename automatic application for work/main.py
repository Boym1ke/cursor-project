import sys
import datetime
import tkinter as tk
from tkinter import messagebox
import process_tops_costs_file
import readexcel2txt
import xml下载

def show_disclaimer():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    disclaimer_text = (
        "作者 / Author: Mai Jiaming\n\n"
        "免责声明 / Disclaimer:\n"
        "本脚本作者不对本次脚本运行所造成的不良后果负责，\n"
        "脚本使用者在这次脚本使用承担所有责任。\n"
        "The author of this script is not responsible for any consequences caused by running this script.\n"
        "The user of this script assumes all responsibility for its use.\n\n"
        "点击确认继续。/ Click OK to continue."
    )
    
    result = messagebox.askokcancel("脚本运行确认 / Script Execution Confirmation", disclaimer_text)
    root.destroy()
    return result

def log_error(message):
    error_file = 'error.txt'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(error_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def run_function(module, name):
    print(f"正在运行 {name}...")
    try:
        module.main()
        print(f"{name} 运行完成。")
        return True
    except Exception as e:
        error_message = f"运行 {name} 时出错:\n{str(e)}"
        print(error_message)
        log_error(error_message)
        return False

def main():
    # 显示免责声明弹窗
    if not show_disclaimer():
        print("用户取消了脚本运行。")
        input("按回车键退出...")
        return

    # 按顺序运行函数
    modules = [
        (process_tops_costs_file, "process_tops_costs_file"),
        (readexcel2txt, "readexcel2txt"),
        (xml下载, "xml下载")
    ]

    for module, name in modules:
        if not run_function(module, name):
            print(f"{name} 运行失败。")
            input("按回车键退出...")
            return

    print("所有脚本已成功运行完毕。")
    input("按回车键退出...")

if __name__ == "__main__":
    main()