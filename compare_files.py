import pandas as pd
import os
from openpyxl.utils import get_column_letter

def compare_files(file1, file2):
    # 读取文件
    if file1.endswith('.xlsx'):
        df1 = pd.read_excel(file1)
    else:
        df1 = pd.read_csv(file1)
    
    if file2.endswith('.xlsx'):
        df2 = pd.read_excel(file2)
    else:
        df2 = pd.read_csv(file2)
    
    # 确保两个DataFrame有相同的列
    common_columns = df1.columns.intersection(df2.columns)
    df1 = df1[common_columns]
    df2 = df2[common_columns]
    
    # 比较数据框
    comparison = df1.compare(df2)
    
    # 如果比较结果为空，返回一个提示
    if comparison.empty:
        return "两个文件完全相同。", None
    
    # 重新格式化比较
    result = []
    for idx, row in comparison.iterrows():
        for col_idx, col in enumerate(comparison.columns.levels[0]):
            if not pd.isna(row[col]['self']) or not pd.isna(row[col]['other']):
                cell = f'{get_column_letter(col_idx + 1)}{idx + 2}'  # +2 因为Excel从1开始计数，且有表头
                result.append({
                    '位置': cell,
                    'file1': row[col]['self'],
                    'file2': row[col]['other']
                })
    
    result_df = pd.DataFrame(result)
    
    # 生成Excel文件
    output_path = 'comparison_result.xlsx'
    with pd.ExcelWriter(output_path) as writer:
        result_df.to_excel(writer, sheet_name='Comparison', index=False)
        df1.to_excel(writer, sheet_name='File1', index=False)
        df2.to_excel(writer, sheet_name='File2', index=False)
    
    return "比较完成，请下载结果文件。", output_path
