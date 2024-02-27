# "C:\test files\climate analysis\data\rainfall raw data\" 폴더의 엑셀 파일들을 병합한다. 
# 파일 이름 형식은 rainfall_data_[###]_[####].csv 이며, ###는 지역 코드, ####는 년도를 나타낸다.
# 병합된 파일은 rainfall_data.csv로 저장된다.

import os
import pandas as pd

# 파일 경로
file_path = "C:/test files/climate analysis/data/rainfall raw data/"

# 파일 목록
file_list = os.listdir(file_path)

# 파일 병합
rainfall_data = pd.DataFrame()
for file in file_list:
    if file.startswith("rainfall_data_"):
        data = pd.read_csv(file_path + file, encoding='ISO-8859-1')  # specify encoding here
        rainfall_data = pd.concat([rainfall_data, data])
# 파일 저장
rainfall_data.to_csv(file_path + "rainfall_data.csv", index=False)

print("파일 병합 완료")

# rainfall_data.csv 파일을 열어서 내용을 확인한다.
# rainfall_data.csv 파일의 내용을 확인한다.
print(rainfall_data.head())
print(rainfall_data.tail())
print(rainfall_data.info())
print(rainfall_data.describe())
print(rainfall_data.shape)
print(rainfall_data.columns)
print(rainfall_data.index)
print(rainfall_data.dtypes)
print(rainfall_data.isnull().sum())
print(rainfall_data.isnull().sum().sum())
print(rainfall_data.isna().sum())

