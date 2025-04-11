import csv
import json
import uuid

# CSV 파일 경로 설정
csv_file_path = 'C:/Users/only4/OneDrive/바탕 화면/서울특별시 서초구_흡연시설 현황_20240617.csv'

# 변환된 JSON 파일 저장 경로 설정
json_file_path = 'C:/Users/only4/OneDrive/바탕 화면/smoking_area_seocho_bulk.json'

# Elasticsearch에서 사용할 인덱스 이름 정의
index_name = 'smoking_area_seocho_converted'

# ID 생성 방식 선택: 'increment'는 숫자 증가 방식, 'uuid'는 고유 문자열 방식
id_mode = 'increment'

# CSV 파일을 열고 동시에 JSON 출력 파일도 열기
# CSV는 윈도우에서 기본 인코딩인 'cp949' 사용 (UTF-8 오류 방지)
with open(csv_file_path, 'r', encoding='cp949') as csv_file, open(json_file_path, 'w', encoding='utf-8') as json_file:
    # CSV 파일을 딕셔너리 형태로 읽기
    reader = csv.DictReader(csv_file)

    # ID 증가용 카운터 초기값 (increment 모드에서 사용)
    counter = 1

    # CSV의 각 행마다 반복
    for row in reader:
        # 선택된 ID 생성 방식에 따라 _id 값을 결정
        if id_mode == 'increment':
            doc_id = str(counter)  # 숫자 기반 ID
        elif id_mode == 'uuid':
            doc_id = str(uuid.uuid4())  # 고유 문자열 ID

        # Elasticsearch Bulk API 형식에 맞춘 메타데이터 작성
        meta = {
            "index": {
                "_index": index_name,  # 인덱스 이름 지정
                "_id": doc_id          # 문서 고유 ID 설정
            }
        }

        # 메타데이터 라인을 JSON 형식 문자열로 기록
        json_file.write(json.dumps(meta, ensure_ascii=False) + "\n")

        # 실제 문서 내용도 JSON 문자열로 기록
        json_file.write(json.dumps(row, ensure_ascii=False) + "\n")

        # 카운터 증가 (increment 모드일 경우)
        counter += 1
