import time
import pyautogui

def lock_computer():
    # 倒计时15分钟（900秒）
    print("15分钟倒计时开始...")
    time.sleep(900)
    
    # 按下Win + L
    print("锁定计算机...")
    pyautogui.hotkey('win', 'l')

if __name__ == "__main__":
    lock_computer()