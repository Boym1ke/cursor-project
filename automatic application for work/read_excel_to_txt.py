import win32com.client
import os

def read_excel_and_write_txt(excel_file, txt_file):
    # 使用Excel应用程序打开文件
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # 不显示Excel窗口
    workbook = excel.Workbooks.Open(excel_file)
    sheet = workbook.Sheets(1)  # 假设我们要读取第一个工作表

    # 获取B3单元格开始到最后一个有内容的A列单元格对应的B列单元格
    urls = []
    row = 3
    while sheet.Cells(row, 1).Value:  # 检查A列是否有值
        cell_value = sheet.Cells(row, 2).Value
        if cell_value:
            urls.append(str(cell_value))
        row += 1

    # 关闭Excel文件
    workbook.Close()
    excel.Quit()

    # 清空并写入readurl.txt文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(f"{url}\n")

    print(f"已成功将{len(urls)}个URL写入到{txt_file}文件中。")

def main():
    # 设置文件路径
    excel_file = r'C:\data\TOPS_Costs url.xlsx'
    txt_file = r'C:\data\readurl.txt'
    
    read_excel_and_write_txt(excel_file, txt_file)

if __name__ == "__main__":
    main()