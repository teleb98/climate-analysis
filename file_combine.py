# "C:\test files\climate analysis\data\rainfall raw data\test" 폴더의 엑셀 파일들을 병합한다. 
# 파일 이름 형식은 rainfall_data_[##]_[####].csv 또는 rainfall_data_[###]_[####].csv 이며, ###는 지역 코드, ####는 년도를 나타낸다.
# 파일명을 분석해서 rainfall_data_[##]_[####].csv 또는 rainfall_data_[###]_[####].csv 데이터에서 [###]인 같은 지역 코드 별로 나눠서 파일 병합
# 병합된 파일은 rainfall_data_[##]_[####].csv 또는 rainfall_data_[###].csv로 저장한다.

import pandas as pd
import glob
import os

# 파일 경로 설정
folder_path = 'C:/test files/climate analysis/data/rainfall raw data/'

# output 폴더 생성
output_folderpath = os.path.join(folder_path, 'output')
if not os.path.exists(output_folderpath):
    os.makedirs(output_folderpath)
  
file_pattern = 'rainfall_data_*.csv'
file_path_pattern = os.path.join(folder_path, file_pattern)

# 파일 목록 가져오기
file_list = glob.glob(file_path_pattern)

# 지역 코드별로 데이터 프레임 저장
data_frames = {}

for file in file_list:
    # 파일명에서 지역 코드와 년도 추출
    base_name = os.path.basename(file)
    region_code, year = base_name[len('rainfall_data_'):].split('_')[0], base_name.split('_')[-1].split('.')[0]

    # endording 설정에 따라 파일 읽기
    df = pd.read_csv(file, encoding='ISO-8859-1')
    
    # 같은 지역 코드의 데이터 프레임 병합
    if region_code in data_frames:
        data_frames[region_code] = pd.concat([data_frames[region_code], df], ignore_index=True)
    else:
        data_frames[region_code] = df

# output_folderpath에 병합된 데이터 저장
for region_code, df in data_frames.items():
    output_file = os.path.join(output_folderpath, f'rainfall_data_{region_code}.csv')
    df.to_csv(output_file, index=False, encoding='ISO-8859-1')
    print(f'{output_file} 파일이 생성되었습니다.')

print("파일 병합이 완료되었습니다.")
