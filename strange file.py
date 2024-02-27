import os
import pandas as pd

# 폴더 경로
folder_path = r'C:\test files\climate analysis\data\csv3'
# 폴더 내 파일명 리스트
file_list = os.listdir(folder_path)

# 파일명, 파일 크기, 파일 생성일자를 저장할 리스트
file_name_list = []
file_size_list = []
file_create_date_list = []

# 파일명, 파일 크기, 파일 생성일자를 리스트에 저장
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    file_name_list.append(file_name)
    file_size_list.append(os.path.getsize(file_path))
    # Unix 타임스탬프를 올바른 날짜 시간 형식으로 변환
    file_create_date_list.append(pd.to_datetime(os.path.getctime(file_path), unit='s'))

# 데이터프레임 생성
df = pd.DataFrame({
    '파일명': file_name_list,
    '파일 크기': file_size_list,
    '파일 생성일자': file_create_date_list
})

# 데이터프레임을 엑셀 파일로 저장
excel_file_path = r'C:\test files\climate analysis\data\strange file.xlsx'
df.to_excel(excel_file_path, index=False)

# 파일 크기 변동 여부 확인 및 업데이트
df['이전 파일 크기'] = df['파일 크기'].shift(1)  # 이전 파일 크기
df['크기 변동 여부'] = df.apply(lambda row: '크기가 크게 변동' if row['이전 파일 크기'] and row['파일 크기'] < row['이전 파일 크기'] * 0.95 else '변동 없음', axis=1)
df.drop('이전 파일 크기', axis=1, inplace=True)  # 이제 불필요한 '이전 파일 크기' 컬럼 제거
df.to_excel(excel_file_path, index=False)

"""
# 아래 파일들은 C:\test files\climate analysis\data\csv3 폴더에서 C:\test files\climate analysis\data\csv3\moved 폴더로 이동
move_file_list = [
    'rainfall_data_135_2014.csv', 'rainfall_data_135_2019.csv', 'rainfall_data_135_2023.csv', 'rainfall_data_136_1974.csv', 'rainfall_data_136_1975.csv', 'rainfall_data_136_1979.csv', 'rainfall_data_136_1980.csv', 'rainfall_data_136_1981.csv', 'rainfall_data_136_1982.csv', 'rainfall_data_136_1997.csv', 'rainfall_data_136_2000.csv', 'rainfall_data_136_2001.csv', 'rainfall_data_136_2002.csv', 'rainfall_data_211_2019.csv', 'rainfall_data_211_2020.csv', 'rainfall_data_235_2019.csv', 'rainfall_data_235_2020.csv', 'rainfall_data_235_2021.csv', 'rainfall_data_235_2022.csv', 'rainfall_data_247_1975.csv', 'rainfall_data_247_2011.csv', 'rainfall_data_247_2012.csv', 'rainfall_data_247_2013.csv', 'rainfall_data_247_2014.csv', 'rainfall_data_248_2023.csv', 'rainfall_data_277_2018.csv', 'rainfall_data_277_2019.csv', 'rainfall_data_277_2020.csv', 'rainfall_data_278_1997.csv', 'rainfall_data_278_2010.csv', 'rainfall_data_278_2011.csv', 'rainfall_data_278_2012.csv', 'rainfall_data_284_1984.csv', 'rainfall_data_284_1985.csv', 'rainfall_data_284_1986.csv', 'rainfall_data_284_1987.csv', 'rainfall_data_284_2000.csv', 'rainfall_data_288_2022.csv', 'rainfall_data_288_2023.csv'
]

# 파일 이동
for file_name in move_file_list:
    file_path = os.path.join(folder_path, file_name)
    moved_folder_path = os.path.join(folder_path, 'moved')
    if not os.path.exists(moved_folder_path):
        os.mkdir(moved_folder_path)
    moved_file_path = os.path.join(moved_folder_path, file_name)
    os.rename(file_path, moved_file_path)
    print(f'{file_name} 파일을 {moved_file_path}로 이동')
"""