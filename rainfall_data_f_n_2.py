import time
import requests
import xml.etree.ElementTree as ET
import csv
import os

# csv 파일 저장 시 한글이 깨지지 않도록 encoding='utf-8'으로 설정

# API 정보
api_url = "https://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
# api_key = "XXPpuUQgJtp1l31ZSrkdw8chjKzvFiTsV0WnzolIlNTZwcDFFGFevVz3BYDkySWrEQnvsI+LsawoN5Ay/L8Fpw=="
# api_key = "rxkMDfW0sUp0bKK69Pm+AFqVZKLpE1sLJbvpFtHjG8VeCyt700ixR+wHleQc4LfEaXAdo5tqJQQuKaMTLiieSw=="
# api_key = "FlAVoLGfl53tXvI927Y78uTmXTk9h0QhiaLHx0S4mOe/+odeYMCNlYqFfMq2Vtt0PQxob5IaZVz+rUax8TDtBQ=="
# api_key = "0M7+jKgHrFh6GfRh5VsZUnXcxY3axyqRZsLWG7ZR39cm0H79GLAiJDOz4wwuakeAU/GTEZQGERetTwvNMo25Tg=="
# api_key = "c62GDjndFHkhPTvVlVE4HTrNTTIWMmvCp+mZNjOXf6FPqkBnTWNfVpoCURQsfOIhuwSIuXr6RrRjtjA3M7sjRw=="
# api_key = "WCVWTAlB+SNJYlD4RgiLnD1f7JmGetBK70zOpd3bjDA65QpAy+/SqNHAGgE+awb2Q9IuqaGHIaxkBsIuLNBmGQ=="
api_key = "swGAvAFGRGGL5VjnIExWlSui70kGtJLTmpfM7ENmgO7RGBavBBWcADQiYu4qIJLT9XnZFPBVvb2smYxkilYVRg=="
# api_key = "GG55qjsKRL88I5Y64fXsjpcn1SxGoZ6R5XatGfjgQ2E4xJA2Fp05y/Eu/vHtCQcE9feo/7eQNoslqshDekELvg=="
# api_key = "4z1aQHnp44sfEm8MWnFkx3JBvcwoQ5n0RsCwMScreJRwe7+osEbLnFNrXHw+hy7Cc1DBEyVT3bV5UfVSbydYgA=="
# api_key = "amIPR7WhR+QAdzAbUeVDZ/88sdRd7Vzl/kAMvEyAz0DJLLQbxDfxXqxNg19z6dBHpfm2KlMWkOx2qKyhpd31Jw=="

# 모든 관측소 ID 목록
stnIds_list = [                    
    90
]

# 관측소별 데이터 시작 날짜 정보 (전체 관측소 반영)
start_dates = {
    90: [1968, 1, 1], 93: [2016, 10, 1], 95: [1988, 1, 1], 98: [1998, 2, 1],
    99: [2001, 12, 7], 100: [1971, 7, 15], 101: [1966, 1, 1], 102: [2000, 11, 1],
    104: [2008, 7, 28], 105: [1911, 10, 3], 106: [1992, 5, 1], 108: [1907, 10, 1],
    112: [1904, 8, 29], 114: [1971, 9, 6], 115: [1938, 8, 10], 119: [1964, 1, 1],
    121: [1994, 12, 1], 127: [1972, 1, 1], 129: [1968, 1, 1], 130: [1971, 1, 12],
    131: [1967, 1, 1], 133: [1969, 1, 1], 135: [1937, 1, 11], 136: [1973, 1, 1],
    137: [2002, 1, 1], 138: [1943, 1, 1], 140: [1968, 1, 1], 143: [1907, 1, 31],
    146: [1918, 6, 23], 152: [1932, 1, 6], 155: [1985, 7, 1], 156: [1939, 5, 1],
    159: [1904, 4, 9], 162: [1968, 1, 1], 165: [1904, 4, 8], 168: [1942, 3, 1],
    169: [1997, 1, 1], 170: [1971, 1, 31], 172: [2010, 12, 1], 174: [2011, 4, 1],
    177: [2015, 11, 3], 184: [1923, 5, 1], 185: [1988, 1, 1], 188: [1971, 7, 15],
    189: [1961, 1, 1], 192: [1969, 3, 1], 201: [1972, 1, 11], 202: [1972, 1, 11],
    203: [1972, 1, 11], 211: [1971, 12, 1], 212: [1971, 9, 27], 216: [1985, 8, 1],
    217: [2010, 8, 6], 221: [1972, 1, 11], 226: [1972, 1, 9], 232: [1972, 1, 8],
    235: [1972, 1, 24], 236: [1972, 1, 9], 238: [1972, 1, 9], 239: [2019, 5, 31],
    243: [1972, 3, 1], 244: [1970, 6, 2], 245: [1970, 1, 5], 247: [1972, 1, 4],
    248: [1988, 1, 1], 251: [2007, 11, 1], 252: [2007, 11, 26], 253: [2008, 2, 13],
    254: [2008, 7, 16], 255: [2008, 12, 26], 257: [2008, 12, 26], 258: [2010, 2, 8],
    259: [2009, 11, 10], 260: [1972, 1, 21], 261: [1971, 2, 3], 262: [1972, 1, 22],
    263: [2010, 6, 21], 264: [2010, 6, 21], 266: [2011, 1, 1], 268: [2014, 5, 9],
    271: [1988, 1, 1], 272: [1972, 11, 28], 273: [1973, 1, 1], 276: [2010, 9, 1],
    277: [1972, 1, 3], 278: [1973, 1, 1], 279: [1973, 1, 1], 281: [1972, 1, 21],
    283: [2010, 8, 6], 284: [1972, 1, 24], 285: [1973, 1, 1], 288: [1973, 1, 1],
    289: [1972, 3, 30], 294: [1972, 1, 24], 295: [1972, 1, 24],
}
"""
{ 90:속초, 93:북춘천, 95:철원, 98:동두천, 99:파주, 100:대관령, 101:춘천, 102:백령도, 104:북강릉, 105:강릉, 106:동해, 108:서울, 112:인천, 114:원주, 
  115:울릉도, 119:수원, 121:영월, 127:충주, 129:서산, 130:울진, 131:청주, 133:대전, 135:추풍령, 136:안동, 137:상주, 138:포항, 140:군산, 143:대구, 
  146:전주, 152:울산, 155:창원, 156:광주, 159:부산, 162:통영, 165:목포, 168:여수, 169:흑산도, 170:완도, 172:고창, 174:순천, 177:홍성, 184:제주, 185:고산, 
  188:성산, 189:서귀포, 192:진주, 201:강화, 202:양평, 203:이천, 211:인제, 212:홍천, 216:태백, 217:정선군, 221:제천, 226:보은, 232:천안, 235:보령, 
  236:부여, 238:금산, 239:세종, 243:부안, 244:임실, 245:정읍, 247:남원, 248:장수, 251:고창군, 252:영광군, 253:김해시, 254:순창군, 255:북창원, 257:양산시, 
  258:보성군, 259:강진군, 260:장흥, 261:해남, 262:고흥, 263:의령군, 264:함양군, 266:광양시, 268:진도군, 271:봉화, 272:영주, 273:문경, 276:청송군, 
  277:영덕, 278:의성, 279:구미, 281:영천, 283:경주시, 284:거창, 285:합천, 288:밀양, 289:산청, 294:거제, 295:남해 }
"""

# 1973년부터 2022년까지 50년간의 데이터 수집, 10년 단위로 API 호출하여 저장
# start_year = 1973
# end_year = 2023
def get_rainfall_data(api_url, api_key, stnId, start_year, end_year):
    rainfall_data = []
    for year in range(start_year, end_year):
        for month in range(1, 13):
            for day in range(1, 32):
                # 각 관측소별 데이터 시작 날짜와 비교하여 스킵 조건 추가
                start_date = start_dates.get(stnId)
                if start_date:
                    # 시작 날짜 이전이면 스킵
                    if (year, month, day) < tuple(start_date):
                        continue

                params = {
                    'serviceKey': api_key,
                    'pageNo': '1',
                    'numOfRows': '999',
                    'dataType': 'XML',
                    'dataCd': 'ASOS',
                    'dateCd': 'HR',
                    'startDt': f'{year}{month:02}{day:02}',
                    'startHh': '01',
                    'endDt': f'{year}{month:02}{day:02}',
                    'endHh': '23',
                    'stnIds': str(stnId)
                } 
                response = requests.get(api_url, params=params)
                time.sleep(0.1)  # API 요청 사이 딜레이
                print(response.status_code)            
                print(response.content)

                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    for item in root.findall('.//item'):
                        rn = item.find('rn')
                        tm = item.find('tm')
                        stnNm = item.find('stnNm')
                        if rn is not None and tm is not None and stnNm is not None:
                            rainfall_data.append([stnNm.text, tm.text, rn.text])
    return rainfall_data

# def get_rainfall_data(api_url, api_key, stnId, start_year, end_year):
#     rainfall_data = []
#     for year in range(start_year, end_year):
#         for month in range(1, 13):        
#             for day in range(1, 32):
#                 params = {
#                     'serviceKey': api_key,
#                     'pageNo': '1',
#                     'numOfRows': '999',
#                     'dataType': 'XML',
#                     'dataCd': 'ASOS',
#                     'dateCd': 'HR',
#                     'startDt': f'{year}{month:02}{day:02}',
#                     'startHh': '01',
#                     'endDt': f'{year}{month:02}{day:02}',
#                     'endHh': '23',
#                     'stnIds': str(stnId)
#                 }
#                 response = requests.get(api_url, params=params)
#                 # response delay를 제공하여 200 오류를 발생시키지 않도록 함
#                 time.sleep(0.1)
#                 print(response.status_code)            
#                 print(response.content) 

#                 if response.status_code == 200:
#                     root = ET.fromstring(response.content)
#                     for item in root.findall('.//item'):
#                         rn = item.find('rn')
#                         tm = item.find('tm')
#                         stnNm = item.find('stnNm')
#                         if rn is not None and tm is not None and stnNm is not None:
#                             rainfall_data.append([stnNm.text, tm.text, rn.text])
#     return rainfall_data

# CSV 파일로 저장할 디렉토리 설정
directory = r'C:\test files\climate analysis\data\csv3'
if not os.path.exists(directory):
    os.makedirs(directory)

# 폴더에 file이 있는지 확인하고 있으면 skip 하는 코드 추가
for stnId in stnIds_list:
    # for start_year in range(1973, 2023, 1):
    for start_year in range(1973, 2023, 1):        
        end_year = start_year + 1
        csv_file_path = os.path.join(directory, f'rainfall_data_{stnId}_{end_year}.csv')

        if os.path.exists(csv_file_path):
            print(f"관측소 ID {stnId}의 강수량 데이터가 '{csv_file_path}'에 이미 저장되어 있습니다.")
            continue
        else:
            rainfall_data = get_rainfall_data(api_url, api_key, stnId, start_year, end_year)
            # 관측소별로 CSV 파일로 저장
            with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Station Name', 'Time', 'Rainfall'])  # 컬럼 헤더 추가
                writer.writerows(rainfall_data)
            print("관측소 ID {stnId}의 강수량 데이터가 '{csv_file_path}'에 저장되었습니다.")    