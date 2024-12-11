import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('测试窗口')
        self.setGeometry(100, 100, 300, 200)
        
        button = QPushButton('测试按钮', self)
        button.move(100, 80)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = TestWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"错误: {str(e)}")
        input("按回车键退出...")  # 这样可以看到错误信息 