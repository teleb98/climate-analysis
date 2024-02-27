import pandas as pd
import os
import glob

# 폴더 경로 설정 (여기서는 실제 환경에 맞게 수정해야 함)
folder_path = "C:/test files/climate analysis/data/rainfall raw data/output/test"

# 해당 폴더 내의 모든 CSV 파일을 찾음
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

for file in csv_files:
    # 파일 읽기
    df = pd.read_csv(file, encoding='utf-8-sig')  # 필요에 따라 인코딩 조정
    
    # 3시간 강수량 합산 계산
    df['3hr_Rainfall_Sum'] = df.groupby(['Station Name', 'Year', 'Month', 'Day'])['Rainfall'].transform(lambda x: x.rolling(window=3, min_periods=1).sum())
    
    # 극한 호우 조건에 따라 '극한 호우' 컬럼 생성
    df['Extreme Rainfall'] = ((df['Rainfall'] >= 50) & (df['3hr_Rainfall_Sum'] >= 90)) | (df['Rainfall'] >= 72)
    df['Extreme Rainfall'] = df['Extreme Rainfall'].map({True: '예', False: '아니오'})
    
    # 파일 이름 분리 (확장자 제외)
    base_name = os.path.basename(file)
    name_part = os.path.splitext(base_name)[0]
    
    # 변경된 데이터를 새 파일로 저장 (원본 파일 이름에 "_updated" 접미사 추가)
    updated_file_name = f"{name_part}_updated.csv"
    updated_file_path = os.path.join(folder_path, updated_file_name)

    df.to_csv(updated_file_path, index=False, encoding='utf-8-sig')  # 한글을 포함할 경우 'utf-8' 인코딩 사용    

print("모든 파일이 성공적으로 업데이트되었습니다.")
