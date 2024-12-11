import sys
import os
import traceback
import logging
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QTextEdit, QPushButton, QLabel, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QMessageBox, QProgressDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import win32com.client
import pythoncom
import time

# 获取程序所在的目录路径
PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__))

# 简化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(PROGRAM_DIR, 'app.log'), 'w', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def get_log_path():
    """获取日志文件路径"""
    try:
        if getattr(sys, 'frozen', False):
            program_dir = os.path.dirname(sys.executable)
        else:
            program_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(program_dir, 'error.txt')
    except:
        return 'error.txt'

def log_error(error_msg):
    """记录错误到error.txt文件"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_file = get_log_path()
        
        os.makedirs(os.path.dirname(error_file), exist_ok=True)
        
        with open(error_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] ERROR:\n{error_msg}\n{'='*50}\n")
            f.flush()
    except Exception as e:
        print(f"写入错误日志失败: {str(e)}")
        print(f"尝试写入的路径: {get_log_path()}")

def connect_outlook(max_retries=3):
    """尝试连接 Outlook，带重试机制"""
    for attempt in range(max_retries):
        try:
            log_error(f"尝试连接 Outlook (第 {attempt + 1} 次)")
            outlook = win32com.client.DispatchEx("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            return outlook, namespace
        except Exception as e:
            log_error(f"连接尝试 {attempt + 1} 失败: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
    return None, None

def check_outlook_availability():
    """检查 Outlook 是否可用"""
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.DispatchEx("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        del namespace
        del outlook
        pythoncom.CoUninitialize()
        return True
    except Exception as e:
        log_error(f"Outlook 可用性检查失败: {str(e)}")
        return False

def main():
    try:
        logger.info("程序开始运行")
        log_error("程序开始运行")
        
        # 创建应用实例
        app = QApplication(sys.argv)
        logger.info("QApplication 创建成功")
        
        # 设置应用样式
        app.setStyle('Fusion')
        logger.info("应用样式设置完成")
        
        # 创建并显示主窗口
        main_window = MyerQuery()
        logger.info("主窗口创建成功")
        
        main_window.show()
        logger.info("主窗口显示成功")
        
        # 进入事件循环
        return app.exec_()
        
    except Exception as e:
        error_msg = f"主程序错误: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        log_error(error_msg)
        
        try:
            # 尝试显示错误消息框
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
            
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("程序启动失败")
            error_msg.setInformativeText(str(e))
            error_msg.setWindowTitle("错误")
            error_msg.exec_()
        except Exception as dialog_error:
            # 如果无法显示消息框，则打印到控制台和错误日志
            error_msg = f"无法显示错误对话框: {str(dialog_error)}\n{traceback.format_exc()}"
            print(error_msg)
            log_error(error_msg)
        
        return 1

class MyerQuery(QMainWindow):
    def __init__(self):
        logger.info("初始化 MyerQuery 类")
        try:
            super().__init__()
            if not check_outlook_availability():
                QMessageBox.warning(
                    self,
                    "警告",
                    "无法连接到 Outlook。请确保：\n"
                    "1. Outlook 已安装并正确配置\n"
                    "2. Outlook 已经运行并登录\n"
                    "3. 没有被安全策略限制"
                )
            # 添加排序状态追踪
            self.current_sort_column = -1
            self.current_sort_order = Qt.AscendingOrder
            self.initUI()
            logger.info("MyerQuery 初始化完成")
        except Exception as e:
            logger.error(f"初始化错误: {str(e)}\n{traceback.format_exc()}")
            self.show_error("程序初始化失败", str(e))
    
    def show_error(self, title, message):
        """显示错误消息框并记录到文件"""
        QMessageBox.critical(self, title, message)
        log_error(f"{title}: {message}")
        
    def initUI(self):
        try:
            # 设置窗口基本属性
            self.setWindowTitle('Myer卡车提货时间查询                                                Program Author: Mai Jiaming')
            self.setGeometry(100, 100, 1000, 800)
            
            # 创建中央窗口部件
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # 创建说明标签
            instruction = QLabel('请输入柜号(用逗号分隔):')
            instruction.setFont(QFont('Arial', 10))
            layout.addWidget(instruction)
            
            # 创建输入框
            self.input_box = QTextEdit()
            self.input_box.setMaximumHeight(100)
            self.input_box.setFont(QFont('Arial', 10))
            layout.addWidget(self.input_box)
            
            # 创建按钮布局
            button_layout = QHBoxLayout()
            
            # 创建查询按钮
            self.query_btn = QPushButton('查询')
            self.query_btn.setFont(QFont('Arial', 10))
            self.query_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.query_btn.clicked.connect(self.perform_query)
            button_layout.addWidget(self.query_btn)
            
            # 创建清空按钮
            self.clear_btn = QPushButton('清空结果')
            self.clear_btn.setFont(QFont('Arial', 10))
            self.clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.clear_btn.clicked.connect(self.clear_results)
            button_layout.addWidget(self.clear_btn)
            
            # 添加按钮布局到主布局
            layout.addLayout(button_layout)
            
            # 创建结果表格
            self.result_table = QTableWidget()
            self.result_table.setColumnCount(4)
            self.result_table.setHorizontalHeaderLabels(['柜号', '预约状态', '预约时间', 'RDC'])
            self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            # 添加表头点击排序功能
            self.result_table.horizontalHeader().setSortIndicatorShown(True)
            self.result_table.horizontalHeader().sectionClicked.connect(self.sort_table)
            
            layout.addWidget(self.result_table)
            
        except Exception as e:
            logger.error(f"UI初始化错误: {str(e)}\n{traceback.format_exc()}")
            self.show_error("UI初始化失败", str(e))
    
    def perform_query(self):
        try:
            # 清空现有结果
            self.result_table.setRowCount(0)
            
            # 获取输入的柜号
            containers = [c.strip() for c in self.input_box.toPlainText().split(',') if c.strip()]
            
            if not containers:
                self.show_error("输入错误", "请输入至少一个柜号")
                return

            # 创建进度对话框
            self.progress = QProgressDialog("正在搜索邮件...", "取消", 0, 100, self)
            self.progress.setWindowTitle("请稍候")
            self.progress.setWindowModality(Qt.WindowModal)
            self.progress.setMinimumDuration(0)  # 立即显示进度条
            self.progress.setAutoClose(False)  # 不自动关闭
            self.progress.setAutoReset(False)  # 不自动重置
            
            # 创建并启动搜索线程
            self.search_thread = SearchThread(containers)
            self.search_thread.result_ready.connect(self.handle_search_result)
            self.search_thread.progress_update.connect(self.update_progress)
            self.search_thread.error_occurred.connect(self.update_progress_text)
            self.search_thread.search_completed.connect(self.search_completed)
            
            # 禁用查询按钮
            self.query_btn.setEnabled(False)
            
            # 启动线程
            self.search_thread.start()
            
        except Exception as e:
            logger.error(f"查询执行错误: {str(e)}\n{traceback.format_exc()}")
            self.show_error("查询执行失败", str(e))

    def handle_search_result(self, data):
        try:
            container = data['container']
            result = data['result']
            
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)
            
            if result:
                # 添加每个单元格时进行错误检查
                for col, value in enumerate([
                    result['container'],
                    result['status'],
                    result['date'],
                    result['rdc']
                ]):
                    item = QTableWidgetItem(str(value))
                    self.result_table.setItem(row, col, item)
            else:
                # 设置未找到结果的行
                values = [container, "未找到匹配信息", "-", "-"]
                for col, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    self.result_table.setItem(row, col, item)
            
            # 确保表格更新
            self.result_table.viewport().update()
            
        except Exception as e:
            self.show_error("处理结果失败", str(e))

    def update_progress(self, value):
        """更新进度条值"""
        if hasattr(self, 'progress'):
            self.progress.setValue(value)

    def update_progress_text(self, text):
        """更新进度条文本"""
        if hasattr(self, 'progress'):
            self.progress.setLabelText(text)

    def search_completed(self):
        """搜索完成时的处理"""
        try:
            if hasattr(self, 'progress'):
                self.progress.close()
            self.query_btn.setEnabled(True)
            
            # 检查结果表格
            total_rows = self.result_table.rowCount()
            
            # 只有在真的没有找到任何结果时才显示提示
            if total_rows == 0:
                QMessageBox.information(self, "搜索结果", "未找到任何匹配结果")
            
        except Exception as e:
            self.show_error("完成搜索处理时出错", str(e))

    def closeEvent(self, event):
        if hasattr(self, 'search_thread') and self.search_thread.isRunning():
            self.search_thread.terminate()
            self.search_thread.wait()
        event.accept()

    def clear_results(self):
        """清空查询结果和输入框"""
        self.result_table.setRowCount(0)
        self.input_box.clear()

    def sort_table(self, column):
        """表格排序方法"""
        try:
            # 如果点击的是同一列，切换排序顺序
            if column == self.current_sort_column:
                self.current_sort_order = Qt.DescendingOrder if self.current_sort_order == Qt.AscendingOrder else Qt.AscendingOrder
            else:
                # 如果是新列，设置为升序
                self.current_sort_column = column
                self.current_sort_order = Qt.AscendingOrder
            
            # 获取所有行的数据
            rows = []
            for row in range(self.result_table.rowCount()):
                row_data = []
                for col in range(self.result_table.columnCount()):
                    item = self.result_table.item(row, col)
                    row_data.append(item.text() if item else "")
                rows.append(row_data)
            
            # 根据选定的列排序
            rows.sort(key=lambda x: x[column], reverse=(self.current_sort_order == Qt.DescendingOrder))
            
            # 更新表格显示
            self.result_table.setUpdatesEnabled(False)  # 暂停更新以提高性能
            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))
            self.result_table.setUpdatesEnabled(True)  # 恢复更新
            
            # 更新排序指示器
            self.result_table.horizontalHeader().setSortIndicator(column, self.current_sort_order)
            
        except Exception as e:
            self.show_error("排序失败", str(e))

class SearchThread(QThread):
    # 定义信号
    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int)
    search_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, containers):
        super().__init__()
        self.containers = containers
        self._outlook = None
        self._namespace = None

    def run(self):
        try:
            pythoncom.CoInitialize()
            
            # 连接 Outlook
            self._outlook, self._namespace = connect_outlook()
            if not self._outlook or not self._namespace:
                raise Exception("无法连接到 Outlook")
            
            self.progress_update.emit(0)
            log_error("开始搜索...")
            
            try:
                # 获取本地 PST 文件中的文件夹
                stores = self._namespace.Stores
                store_count = stores.Count
                
                # 查找本地存储
                local_store = None
                for i in range(1, store_count + 1):
                    store = stores.Item(i)
                    if "Local_Landside_Update" in store.DisplayName:
                        local_store = store
                        break
                
                if not local_store:
                    raise Exception("未找到本地存储文件")
                
                # 获取根文件夹
                root_folder = local_store.GetRootFolder()
                
                # 查找 Landside update 子文件夹
                target_folder = None
                for folder in root_folder.Folders:
                    if folder.Name == "Landside update":
                        target_folder = folder
                        break
                
                if not target_folder:
                    raise Exception("未找到 Landside update 文件夹")
                
                messages = target_folder.Items
                if not messages:
                    raise Exception("没有找到任何邮件")
                
                # 设置时间限制
                cutoff_date = (datetime.now() - timedelta(days=120)).replace(hour=0, minute=0, second=0, microsecond=0)
                
                # 预先过滤邮件
                self.error_occurred.emit("正在预处理邮件...")
                filtered_messages = []
                messages.Sort("[ReceivedTime]", True)
                
                for message in messages:
                    try:
                        received_time = message.ReceivedTime
                        if isinstance(received_time, datetime):
                            received_time = received_time.replace(tzinfo=None)
                        if received_time < cutoff_date:
                            continue
                        
                        subject = message.Subject
                        if ("Appointment Rescheduled" in subject or 
                            "Appointment Approved" in subject):
                            filtered_messages.append({
                                'message': message,
                                'subject': subject,
                                'body': message.Body,
                                'received_time': received_time
                            })
                    except Exception as e:
                        continue
                
                log_error(f"预处理后的邮件数量: {len(filtered_messages)}")
                
                # 创建柜号到结果的映射
                container_map = {container: None for container in self.containers}
                total = len(self.containers)
                processed = 0
                
                # 处理每封邮件
                for msg_data in filtered_messages:
                    try:
                        body = msg_data['body']
                        subject = msg_data['subject']
                        
                        # 找出这封邮件匹配的所有柜号
                        found_containers = [c for c in container_map.keys() 
                                         if c in body and container_map[c] is None]
                        
                        if found_containers and "APPOINTMENT REQUEST - APPROVED" in body:
                            # 提取邮件信息
                            requested_date = ""
                            rdc = ""
                            for line in body.split('\n'):
                                if "REQUESTED DATE:" in line:
                                    requested_date = line.split("REQUESTED DATE:")[1].strip()
                                if "RDC:" in line:
                                    rdc = line.split("RDC:")[1].strip()
                                if requested_date and rdc:
                                    break
                            
                            is_rescheduled = "Appointment Rescheduled" in subject
                            
                            # 更新所有匹配的柜号
                            for container in found_containers:
                                if not container_map[container] or is_rescheduled:
                                    result = {
                                        'container': container,
                                        'status': "已改期" if is_rescheduled else "已批准",
                                        'date': requested_date,
                                        'rdc': rdc
                                    }
                                    container_map[container] = result
                                    self.result_ready.emit({
                                        'container': container,
                                        'result': result
                                    })
                                    processed += 1
                                    
                                    progress = int((processed / total) * 100)
                                    self.progress_update.emit(progress)
                                    self.error_occurred.emit(f"已处理: {processed}/{total}")
                        
                        # 如果所有柜号都找到了结果，提前结束
                        if all(v is not None for v in container_map.values()):
                            break
                            
                    except Exception as e:
                        continue
                
                # 处理未找到结果的柜号
                for container, result in container_map.items():
                    if result is None:
                        self.result_ready.emit({
                            'container': container,
                            'result': None
                        })
                
                self.progress_update.emit(100)
                
            except Exception as e:
                error_msg = f"搜索过程出错: {str(e)}"
                log_error(error_msg)
                self.error_occurred.emit(error_msg)
            
            finally:
                self.search_completed.emit()
                
        except Exception as e:
            error_msg = f"搜索线程出错: {str(e)}"
            log_error(error_msg)
            self.error_occurred.emit(error_msg)
            self.search_completed.emit()
        
        finally:
            if self._namespace:
                del self._namespace
            if self._outlook:
                del self._outlook
            pythoncom.CoUninitialize()

if __name__ == '__main__':
    try:
        logger.info("程序入口点")
        log_error("程序启动")
        exit_code = main()
        logger.info(f"程序结束，退出代码: {exit_code}")
        log_error(f"程序结束，退出代码: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        error_msg = f"未捕获的异常: {str(e)}\n{traceback.format_exc()}"
        logger.critical(error_msg)
        log_error(error_msg)
        print(f"程序崩溃: {str(e)}")
        sys.exit(1)

