import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

def main():
    try:
        print("程序开始运行...")  # 调试信息
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setGeometry(100, 100, 300, 200)
        window.setWindowTitle('测试窗口')
        
        label = QLabel('测试标签', window)
        label.move(100, 80)
        
        window.show()
        print("窗口已显示...")  # 调试信息
        
        return app.exec_()
    except Exception as e:
        print(f"发生错误: {str(e)}")
        input("按Enter继续...")
        return 1

if __name__ == '__main__':
    print("程序入口点...")  # 调试信息
    sys.exit(main()) 