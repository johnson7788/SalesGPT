#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2023/9/18 14:34
# @File  : product.py.py
# @Author: 
# @Desc  :


import pandas as pd

def excel2product():
    """
    excel 生成产品信息文本
    """
    excel = "/Users/admin/Documents/lavector/香水问答/香水问答测试数据集.xlsx"
    data_file = "sample_product_catalog.txt"
    df = pd.read_excel(excel)
    data = []
    for idx, row in df.iterrows():
        content = ""
        for key, value in row.items():
            if key == "链接1":
                continue
            content += f"{key}: {value}\n"
        data.append(content)
    with open(data_file, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line)
            f.write("\n")
    print(f"生成产品信息文本成功，文件路径：{data_file}")


if __name__ == '__main__':
    excel2product()