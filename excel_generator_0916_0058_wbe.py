# 代码生成时间: 2025-09-16 00:58:10
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from tornado.web import RequestHandler, Application, HTTPError
from tornado.ioloop import IOLoop
from tornado.options import define, options

# 定义端口号
define('port', default=8000, help='run on the given port')

class ExcelHandler(RequestHandler):
    """处理生成Excel表格的请求"""
    def get(self):
        # 获取请求参数
        name = self.get_argument('name', default='Untitled')
        num_rows = int(self.get_argument('num_rows', default=10))
        num_cols = int(self.get_argument('num_cols', default=5))

        # 创建工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = 'Generated Excel'

        # 设置字体和对齐方式
        font = Font(bold=True)
        alignment = Alignment(horizontal='center', vertical='center')

        # 填充表格数据
        for row in range(num_rows):
            for col in range(num_cols):
                ws.cell(row=row+1, column=col+1, value=f'Cell {row+1}-{col+1}', font=font, alignment=alignment)

        # 保存工作簿
        filename = f'{name}.xlsx'
        wb.save(filename)

        # 设置响应头
        self.set_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.set_header('Content-Disposition', f'attachment; filename={filename}')

        # 发送文件
        with open(filename, 'rb') as f:
            self.write(f.read())

        # 删除临时文件
        os.remove(filename)

    def write_error(self, status_code, **kwargs):
        "