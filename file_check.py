# "C:\test files\climate analysis\data\csv3\" 폴더 안의 파일들의 이름을 엑셀 파일에 행으로 추가하는 프로그램이다.

import os
from openpyxl import Workbook

# 폴더 경로 설정
folder_path = "C:\\test files\\climate analysis\\data\\csv3\\"

# 새로운 엑셀 워크북 생성
wb = Workbook()
ws = wb.active

# 폴더 내 모든 파일의 파일명을 읽어와서 엑셀 파일의 각 행에 추가
for filename in os.listdir(folder_path):
    ws.append([filename])

# 엑셀 파일 저장
excel_filename = "C:\\test files\\climate analysis\\data\\file_names.xlsx"
wb.save(excel_filename)
