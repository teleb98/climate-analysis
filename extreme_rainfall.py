import pandas as pd
import os
import glob
from tqdm import tqdm

# 폴더 경로 설정
folder_path = r"C:\test files\climate analysis\data\rainfall raw final\output\extreme rain"

"""
# 해당 폴더 내의 모든 CSV 파일을 찾음
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# 빈 데이터프레임 생성
all_data = pd.DataFrame()

for file in csv_files:
    # 파일 읽기
    df = pd.read_csv(file)
    
    # Rainfall 컬럼의 값이 0인 행 제외
    df_filtered = df[df['Rainfall'] > 0]
    
    # 필터링된 데이터를 all_data에 추가
    all_data = pd.concat([all_data, df_filtered], ignore_index=True)

# 병합된 데이터를 새 파일로 저장
output_path = os.path.join(folder_path, "extreme_rainfall.csv")
all_data.to_csv(output_path, index=False, encoding='utf-8-sig')

print("모든 데이터가 성공적으로 병합되어 'extreme_rainfall.csv' 파일에 저장되었습니다.")
"""

# 해당 폴더 내의 모든 xlsx 파일을 찾음
xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

# 빈 데이터프레임 생성
all_data = pd.DataFrame()

# progress bar 생성
for file in xlsx_files:
    # xlsx 파일 읽기
    df = pd.read_excel(file) 
    
    # Rainfall 컬럼의 값이 0인 행 제외
    df_filtered = df[df['Rainfall'] > 0]
    
    # 필터링된 데이터를 all_data에 추가
    all_data = pd.concat([all_data, df_filtered], ignore_index=True)
    
    # progress bar 업데이트
    tqdm.write(f"{file} 파일이 필터링되었습니다.")
    
# 병합된 데이터를 새 xlsx 파일로 저장
output_path = os.path.join(folder_path, "extreme_rainfall.xlsx")
all_data.to_excel(output_path, index=False)

print("모든 데이터가 성공적으로 병합되어 'extreme_rainfall.xlsx' 파일에 저장되었습니다.")
