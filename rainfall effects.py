import requests
import xml.etree.ElementTree as ET
import csv
import os

# startDt = 19730101, endDt = 20221231 을 지정하되 반복해서 100개 row씩 가져오기
def get_rainfall_data(api_url, api_key):
    params = {
        'serviceKey': api_key,  # 인증키
        'pageNo': '1',          # 페이지 번호
        'numOfRows': '100',      # 한 페이지 결과 수
        'dataType': 'XML',      # 응답 데이터 형식
        'dataCd': 'ASOS',       # ASOS 자료 호출
        'dateCd': 'HR',         # 시간 단위 자료 호출
        'startDt': '20100101',  # 시작일
        'startHh': '01',        # 시작시간
        'endDt': '20100630',    # 종료일
        'endHh': '23',          # 종료시간
        'stnIds': '108'         # 서울 지점 번호        
        # 추가적인 매개변수가 필요할 경우 여기에 추가하세요
    }

    response = requests.get(api_url, params=params)
    
    # 응답 상태 확인
    if response.status_code != 200:
        return f"API 호출 실패: 상태 코드 {response.status_code}"

    # XML 응답 파싱
    root = ET.fromstring(response.content)
    rainfall_data = []

    for item in root.findall('.//item'):
        rn = item.find('rn')
        tm = item.find('tm')
        stnNm = item.find('stnNm')
        if rn is not None and tm is not None and stnNm is not None:
            rainfall_data.append([stnNm.text, tm.text, rn.text])
        else:
            rainfall_data.append(['No Data', 'No Data', 'No Data'])

    return rainfall_data

# API 정보
api_url = "https://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
api_key = "XXPpuUQgJtp1l31ZSrkdw8chjKzvFiTsV0WnzolIlNTZwcDFFGFevVz3BYDkySWrEQnvsI%2BLsawoN5Ay%2FL8Fpw%3D%3D"

# 함수 호출
# 실제 환경에서는 아래 코드를 실행해야 합니다.
rainfall_data = get_rainfall_data(api_url, api_key)
# xml을 파싱한 rainfall_data를 저장
# rainfall_data를 C:\test files\climate analysis\data\csv 파일로 저장
directory = r'C:\test files\climate analysis\data\csv'
if not os.path.exists(directory):
    os.makedirs(directory)

with open(os.path.join(directory, 'rainfall_data.csv'), 'w', newline='') as f:
    writer = csv.writer(f)    
    for data in rainfall_data:
        writer.writerow([data])
