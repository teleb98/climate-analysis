# Description: This code is to get rainfall data from API and save it as csv file.
import requests
import xml.etree.ElementTree as ET
import csv
import os

# API 정보
api_url = "https://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
api_key = "XXPpuUQgJtp1l31ZSrkdw8chjKzvFiTsV0WnzolIlNTZwcDFFGFevVz3BYDkySWrEQnvsI+LsawoN5Ay/L8Fpw=="
# api_key = 'XXPpuUQgJtp1l31ZSrkdw8chjKzvFiTsV0WnzolIlNTZwcDFFGFevVz3BYDkySWrEQnvsI%2BLsawoN5Ay%2FL8Fpw%3D%3D'
"""
{ 90:속초, 93:북춘천, 95:철원, 98:동두천, 99:파주, 100:대관령, 101:춘천, 102:백령도, 104:북강릉, 105:강릉, 106:동해, 108:서울, 112:인천, 114:원주, 
  115:울릉도, 119:수원, 121:영월, 127:충주, 129:서산, 130:울진, 131:청주, 133:대전, 135:추풍령, 136:안동, 137:상주, 138:포항, 140:군산, 143:대구, 
  146:전주, 152:울산, 155:창원, 156:광주, 159:부산, 162:통영, 165:목포, 168:여수, 169:흑산도, 170:완도, 172:고창, 174:순천, 177:홍성, 184:제주, 185:고산, 
  188:성산, 189:서귀포, 192:진주, 201:강화, 202:양평, 203:이천, 211:인제, 212:홍천, 216:태백, 217:정선군, 221:제천, 226:보은, 232:천안, 235:보령, 
  236:부여, 238:금산, 239:세종, 243:부안, 244:임실, 245:정읍, 247:남원, 248:장수, 251:고창군, 252:영광군, 253:김해시, 254:순창군, 255:북창원, 257:양산시, 
  258:보성군, 259:강진군, 260:장흥, 261:해남, 262:고흥, 263:의령군, 264:함양군, 266:광양시, 268:진도군, 271:봉화, 272:영주, 273:문경, 276:청송군, 
  277:영덕, 278:의성, 279:구미, 281:영천, 283:경주시, 284:거창, 285:합천, 288:밀양, 289:산청, 294:거제, 295:남해 }
"""
# stnIds = '108'    # 서울
stnIds = '90'       # 속초

start_year = 1988
end_year = start_year + 5
# API 호출 함수 정의
# 19730101 ~ 19731231, 19740101 ~ 19741231, ... , 20220101 ~ 20221231
# 한 번에 가져올 수 있는 row의 수는 1000개
# 한 번에 가져올 수 있는 row의 수를 초과하는 경우는 없다고 가정
# 4년 데이터를 한번에 불러옴
def get_rainfall_data(api_url, api_key, start_year, end_year):
    # 빈 리스트 생성
    rainfall_data = []
    # 1973년 1월 1일부터 2022년 12월 31일까지 4년 단위로 API 호출
    # for year in range(1973, 2023):
    for year in range(start_year, end_year):
        for month in range(1, 13):
            for day in range(1, 32):                
                # API 호출에 필요한 파라미터 정의
                params = {
                    'serviceKey': api_key,
                    'pageNo': '1',          # 페이지 번호
                    'numOfRows': '999',      # 한 페이지 결과 수            
                    'dataType': 'XML',
                    'dataCd': 'ASOS',
                    'dateCd': 'HR',
                    'startDt': f'{year}{month:02}{day:02}',
                    'startHh': '01',        # 시작시간
                    'endDt': f'{year}{month:02}{day:02}',
                    'endHh': '23',          # 종료시간
                    # 'stnIds': '108'
                    'stnIds': stnIds
                }    
     
                # API 호출, timeout 30초이 지나면 에러 발생 및 rainfall_data 엑셀로 저장                                
                response = requests.get(api_url, params=params)                
                print(response.status_code)
                # API 호출에 실패한 경우
                print(response.content)                
                
                if response.status_code != 200:
                    print(f'{year}년도 데이터 호출에 실패했습니다.')
                    # continue
                    # stop
                    break
                # API 호출에 성공한 경우
                else:
                    # XML 응답 파싱            
                    root = ET.fromstring(response.content)                    

                    for item in root.findall('.//item'):
                        rn = item.find('rn')
                        tm = item.find('tm')
                        stnNm = item.find('stnNm')
                        if rn is not None and tm is not None and stnNm is not None:
                            rainfall_data.append([stnNm.text, tm.text, rn.text])
                        else:
                            rainfall_data.append(['No Data', 'No Data', 'No Data'])                    
    # rainfall_data 리스트를 반환
    return rainfall_data

# 함수 호출
# 실제 환경에서는 아래 코드를 실행해야 합니다.
rainfall_data = get_rainfall_data(api_url, api_key, start_year, end_year)
# xml을 파싱한 rainfall_data를 저장
# rainfall_data를 C:\test files\climate analysis\data\csv 파일로 저장
directory = r'C:\test files\climate analysis\data\csv'
if not os.path.exists(directory):
    os.makedirs(directory)

# file 명을 rainfall_data_{year의 data}stnIds.csv로 저장
# with open(os.path.join(directory, f'rainfall_data_{start_year}.csv'), 'w', newline='') as f:
with open(os.path.join(directory, f'rainfall_data_{start_year}_{stnIds}.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    for data in rainfall_data:
        writer.writerow([data])      