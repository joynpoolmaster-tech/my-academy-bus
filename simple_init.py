# simple_init.py - 간단한 초기화 스크립트

import os
import sqlite3
from flask import Flask
from database import db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'

db.init_app(app)

def clean_start():
    """완전히 새로 시작"""
    print("🚀 완전 초기화 시작...")
    
    # 기존 파일들 삭제
    files_to_remove = ['database.db', 'database_backup.db']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ {file} 삭제됨")
    
    with app.app_context():
        try:
            print("📋 테이블 생성 중...")
            
            # 모든 모델을 한 번에 import
            from models import Branch, User, Student, Class, TimeSlot, Vehicle, DispatchResult
            
            # 테이블 생성
            db.create_all()
            print("✅ 모든 테이블 생성 완료!")
            
            # 테이블 목록 확인
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("📋 생성된 테이블:")
            for table in tables:
                print(f"  - {table}")
            
            return True
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

def create_sample_data():
    """샘플 데이터 생성"""
    print("\n👤 샘플 데이터 생성 중...")
    
    with app.app_context():
        try:
            from models import Branch, User, Class, TimeSlot, Vehicle, Student
            from werkzeug.security import generate_password_hash
            from datetime import date
            
            # 지점 생성
            branch = Branch(name='하남본점')
            db.session.add(branch)
            db.session.flush()
            print("✅ 지점 생성: 하남본점")
            
            # 관리자 생성
            admin = User(
                email='admin@test.com',  # username 제거, email 사용
                password_hash=generate_password_hash('admin123'),
                name='관리자',
                phone='010-0000-0000',
                role='master'
            )
            db.session.add(admin)
            print("✅ 관리자 생성: admin@test.com/admin123")
            
            # 기사 생성
            driver = User(
                email='driver1@test.com',  # username 제거, email 사용
                password_hash=generate_password_hash('driver123'),
                name='김기사',
                phone='010-1111-1111',
                role='driver',
                driver_branch_id=branch.id
            )
            db.session.add(driver)
            db.session.flush()
            print("✅ 기사 생성: driver1@test.com/driver123")
            
            # 차량 생성
            vehicle = Vehicle(
                vehicle_number='12가3456',
                capacity=8,
                branch_id=branch.id,
                driver_id=driver.id
            )
            db.session.add(vehicle)
            print("✅ 차량 생성: 12가3456")
            
            # 클래스 생성
            class_obj = Class(
                name='수영1부',
                branch_id=branch.id,
                max_students=8,
                description='초급반'
            )
            db.session.add(class_obj)
            db.session.flush()
            
            # 시간대 생성
            time_slot = TimeSlot(
                class_id=class_obj.id,
                time='14:00'
            )
            db.session.add(time_slot)
            print("✅ 클래스 생성: 수영1부 (14:00)")
            
            # 학생 사용자 생성
            student_user = User(
                email='student1@test.com',  # username 제거, email 사용
                password_hash=generate_password_hash('student123'),
                name='홍길동',
                phone='010-2222-2222',
                role='student'
            )
            db.session.add(student_user)
            db.session.flush()
            
            # 학생 정보 생성
            student = Student(
                user_id=student_user.id,
                branch_id=branch.id,
                branch_name='하남본점',
                class_name='수영1부',
                time_slot='14:00',
                address='서울시 강남구',
                status='approved',
                start_date=date.today()
            )
            db.session.add(student)
            print("✅ 학생 생성: 홍길동")
            
            db.session.commit()
            print("🎉 모든 샘플 데이터 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 샘플 데이터 생성 실패: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 간단한 데이터베이스 초기화")
    print("=" * 50)
    
    if clean_start():
        if create_sample_data():
            print("\n🎊 초기화 완료!")
            print("\n📋 테스트 계정:")
            print("- 관리자: admin@test.com / admin123")
            print("- 기사: driver1@test.com / driver123") 
            print("- 학생: student1@test.com / student123")
            print("\n🚀 이제 python app.py를 실행하세요!")
        else:
            print("\n⚠️ 샘플 데이터 생성 실패")
    else:
        print("\n❌ 초기화 실패")