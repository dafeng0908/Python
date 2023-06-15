#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 22:38:43 2023

@author: zhongdafeng
"""

import tkinter as tk
from tkinter import ttk
import binascii

# 定義程式段位址和大小
program_address = 0
program_size = 0

# 定義資料段位址和大小
data_address = 0
data_size = 0

# 初始化要燒錄的資料
program_data = bytearray()
data = bytearray()

class CSVViewer:
    def __init__(self, master):
        self.master = master
        self.master.geometry('600x400')
        
        self.table = ttk.Treeview(self.master, columns=('col1', 'col2'), show='headings')
        self.table.heading('col1', text='Column 1')
        self.table.heading('col2', text='Column 2')
        
        self.hscrollbar = ttk.Scrollbar(self.master, orient='horizontal', command=self.table.xview)
        self.hscrollbar.pack(side='bottom', fill='x')

        self.vscrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.table.yview)
        self.vscrollbar.pack(side='right', fill='y')

        self.table.configure(xscrollcommand=self.hscrollbar.set, yscrollcommand=self.vscrollbar.set)

        self.table.pack(side='top', fill='both', expand=True)
        
        self.load_button = tk.Button(self.master, text='Load Hex', command=self.load_csv)
        self.load_button.pack(side='bottom', pady=10)
        self.load_button = tk.Button(self.master, text='FW Upgrade', command=self.load_csv)
        self.load_button.pack(side='bottom', pady=10)
    
    def load_csv(self):
        # 讀取 hex 檔案
        with open('sample.hex', 'r') as f:
            # 讀取每一行並解析
            for line in f:
                # 去掉左右兩邊的空格和換行符號等
                line = line.strip()
                # 將行資料轉成 bytes
                try:
                    line_bytes = bytes.fromhex(line)
                except ValueError as e:
                    print(f'Error parsing line {line}: {e}')
                    continue
                # 取得資料長度
                length = line_bytes[0]
                # 取得資料位址
                address = (line_bytes[1] << 8) + line_bytes[2]
                # 取得紀錄型態
                record_type = line_bytes[3]
                # 取得資料
                data = line_bytes[4:-1]
                # 取得校驗和
                checksum = line_bytes[-1]
                # 校驗碼驗證
                calculated_checksum = sum(line_bytes[:-1]) & 0xff
                if calculated_checksum != checksum:
                    print(f'Invalid checksum for line {line}')
                    continue
                # 根據紀錄型態處理資料
                if record_type == 0:
                    # 資料紀錄型態，將資料新增到要燒錄的資料中
                    if address >= program_address:
                        # 計算燒錄資料的位址
                        offset = address - program_address
                        # 擴充套件燒錄資料陣列，使其足夠大小
                    if offset + length > program_size:
                        program_data.extend(bytearray(offset + length - program_size))
                        # 將資料寫入燒錄資料陣列中
                        program_data[offset:offset + length] = data
                elif record_type == 4:
                    # 段紀錄型態，更新段位址
                    data_address = int.from_bytes(data, byteorder='big') << 16
                elif record_type == 5:
                    # 結束紀錄型態，結束解析
                    break
                else:
                    # 未知紀錄型態，忽略
                    continue
                
if __name__ == '__main__':
    root = tk.Tk()
    app = CSVViewer(root)
    root.mainloop()