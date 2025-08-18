# utils/gsheet_route.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 구글시트 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

ROUTE_SHEET_URL = "경로시트_URL_여기에_입력하세요"

def append_route_data(route_list, driver_name, vehicle_no):
    sheet = client.open_by_url(ROUTE_SHEET_URL)
    worksheet = sheet.worksheet("경로저장")

    today = datetime.today().strftime("%Y-%m-%d")

    for r in route_list:
        row = [
            today,
            vehicle_no,
            r["지점명"],
            r.get("반", ""),  # 반이 없으면 공백
            r["시간대"],
            r["이름"],
            r["주소"],
            driver_name,
            "승인"  # 상태는 무조건 승인된 애들임
        ]
        worksheet.append_row(row)
