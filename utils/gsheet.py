import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime

# 🔐 인증 설정
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "../credentials.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
client = gspread.authorize(creds)

# ✅ 수강회원 시트 저장 함수
def append_member_data(sheet_url, data):
    sheet = client.open_by_url(sheet_url).sheet1
    today = datetime.today().strftime("%Y-%m-%d")
    row = [
        data.get("branch", ""),          # A 지점명
        data.get("name", ""),            # B 이름
        today,                           # C 가입일자
        data.get("start_date", ""),      # D 수강 시작일
        data.get("end_date", ""),        # E 수강 종료일
        data.get("extension_count", ""), # F 연장 횟수
        data.get("class_name", ""),      # G 반/클래스
        data.get("time_slot", ""),       # H 시간대
        data.get("address", ""),         # I 주소
        data.get("phone", ""),           # J 휴대전화번호 입력
        data.get("emergency", ""),       # K 비상연락망
        data.get("birth", ""),           # L 생년월일
        data.get("email", ""),           # M 이메일(ID)
        data.get("memo", "")             # N 비고
    ]
    sheet.append_row(row)

# ✅ 기사 시트 저장 함수
def append_driver_data(sheet_url, data):
    sheet = client.open_by_url(sheet_url).sheet1
    row = [
        data.get("branch", ""),      # A 지점명
        data.get("name", ""),        # B 이름
        data.get("time_slot", ""),   # C 시간대
        data.get("address", ""),     # D 주소
        "대기",                      # E 승인여부
        "",                          # F 배정호차
        ""                           # G 비고
    ]
    sheet.append_row(row)
