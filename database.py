# database.py (신규 파일)
# 설명: 순환 참조 오류를 막기 위해, 데이터베이스 연결 객체(db)를
#       독립적으로 관리하는 '중간 다리' 역할을 합니다.

from flask_sqlalchemy import SQLAlchemy

# 먼저 비어있는 db 객체를 만듭니다.
db = SQLAlchemy()
