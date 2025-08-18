# utils/google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime

# Google API 인증 설정
def get_gspread_client():
    """gspread 클라이언트 객체를 반환합니다."""
    try:
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
        return client
    except Exception as e:
        print(f"Google Sheets 인증 실패: {e}")
        return None

def create_spreadsheet_template(client, user_email):
    """지정된 양식으로 새로운 구글 스프레드시트를 생성하고 공유합니다."""
    if not client:
        raise Exception("Google Sheets 클라이언트가 초기화되지 않았습니다.")
    
    # 새 스프레드시트 생성
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    spreadsheet = client.create(f'JOY&POOL 회원 일괄등록 양식 ({timestamp})')

    # 워크시트에 헤더 추가
    worksheet = spreadsheet.sheet1
    worksheet.title = '회원명부'
    headers = [
        '이름', '이메일', '연락처', '비상연락망', '주소',
        '지점명', '클래스명', '시간대', '수강시작일(YYYY-MM-DD)', '수강기간(개월)'
    ]
    worksheet.append_row(headers)
    
    # 생성된 시트를 사용자 이메일과 공유 (편집자 권한)
    spreadsheet.share(user_email, perm_type='user', role='writer')
    
    return spreadsheet.url