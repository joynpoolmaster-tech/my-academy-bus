# init_database.py - 수정된 데이터베이스 테이블 생성 스크립트

from flask import Flask
from database import db
import os

app = Flask(__name__)

# 기본 설정
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'

db.init_app(app)

def init_database():
    """데이터베이스 테이블 생성"""
    
    with app.app_context():
        try:
            print("🚀 데이터베이스 초기화 시작...")
            
            # 기존 데이터베이스 백업 (있는 경우)
            if os.path.exists('database.db'):
                import shutil
                import datetime
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f'database_backup_{timestamp}.db'
                shutil.copy('database.db', backup_name)
                print(f"✅ 기존 데이터베이스 백업: {backup_name}")
            
            # 기존 데이터베이스 파일 삭제 (완전 초기화)
            if os.path.exists('database.db'):
                os.remove('database.db')
                print("🗑️ 기존 데이터베이스 파일 삭제")
            
            # 모델들을 개별적으로 import하여 테이블 생성 순서 제어
            print("📋 모델 import 및 테이블 생성 중...")
            
            # 1. 기본 테이블들 먼저 생성 (외래키 없는 것들)
            from models import Branch
            db.create_all()
            print("  ✅ Branch 테이블 생성")
            
            # 2. User 테이블 생성
            from models import User
            db.create_all()
            print("  ✅ User 테이블 생성")
            
            # 3. Class 테이블 생성
            from models import Class
            db.create_all()
            print("  ✅ Class 테이블 생성")
            
            # 4. TimeSlot 테이블 생성
            from models import TimeSlot
            db.create_all()
            print("  ✅ TimeSlot 테이블 생성")
            
            # 5. Vehicle 테이블 생성
            from models import Vehicle
            db.create_all()
            print("  ✅ Vehicle 테이블 생성")
            
            # 6. Student 테이블 생성
            from models import Student
            db.create_all()
            print("  ✅ Student 테이블 생성")
            
            # 7. DispatchResult 테이블 생성 (마지막에)
            from models import DispatchResult
            db.create_all()
            print("  ✅ DispatchResult 테이블 생성")
            
            print("✅ 모든 데이터베이스 테이블 생성 완료!")
            
            # 생성된 테이블 목록 확인
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("\n📋 생성된 테이블 목록:")
            for table in tables:
                print(f"  - {table}")
                
            return True
            
        except Exception as e:
            print(f"❌ 데이터베이스 초기화 실패: {e}")
            import traceback
            print("📊 상세 오류:")
            traceback.print_exc()
            return False

def create_initial_data():
    """초기 데이터 생성"""
    
    with app.app_context():
        try:
            # models를 여기서 import (테이블 생성 후)
            from models import Branch, User, Class, TimeSlot, Vehicle
            from werkzeug.security import generate_password_hash
            
            print("\n👤 초기 데이터 생성 중...")
            
            # 기본 지점 생성
            if not Branch.query.first():
                default_branch = Branch(name='하남본점')
                db.session.add(default_branch)
                db.session.commit()
                print("✅ 기본 지점 '하남본점' 생성됨")
            
            # 마스터 관리자 생성
            if not User.query.filter_by(username='admin').first():
                master_admin = User(
                    username='admin',
                    email='admin@joypool.com',
                    password_hash=generate_password_hash('admin123'),
                    name='시스템 관리자',
                    phone='010-0000-0000',
                    role='master'
                )
                db.session.add(master_admin)
                db.session.commit()
                print("✅ 마스터 관리자 계정 생성됨 (admin/admin123)")
            
            # 지점 관리자 생성
            branch = Branch.query.first()
            if branch and not User.query.filter_by(username='hanam').first():
                branch_admin = User(
                    username='hanam',
                    email='hanam@joypool.com',
                    password_hash=generate_password_hash('hanam123'),
                    name='하남점장',
                    phone='010-1111-1111',
                    role='admin',
                    branch_id=branch.id
                )
                db.session.add(branch_admin)
                db.session.commit()
                print("✅ 지점 관리자 계정 생성됨 (hanam/hanam123)")
            
            # 샘플 기사 생성
            if branch and not User.query.filter_by(role='driver').first():
                driver1 = User(
                    username='driver1',
                    email='driver1@joypool.com',
                    password_hash=generate_password_hash('driver123'),
                    name='김기사',
                    phone='010-2222-2222',
                    role='driver',
                    driver_branch_id=branch.id
                )
                db.session.add(driver1)
                
                driver2 = User(
                    username='driver2',
                    email='driver2@joypool.com',
                    password_hash=generate_password_hash('driver123'),
                    name='이기사',
                    phone='010-3333-3333',
                    role='driver',
                    driver_branch_id=branch.id
                )
                db.session.add(driver2)
                db.session.commit()
                print("✅ 샘플 기사 2명 생성됨 (driver1/driver123, driver2/driver123)")
            
            # 샘플 차량 생성
            if branch and not Vehicle.query.first():
                drivers = User.query.filter_by(role='driver').all()
                
                vehicle1 = Vehicle(
                    vehicle_number='12가3456',
                    capacity=8,
                    branch_id=branch.id,
                    driver_id=drivers[0].id if drivers else None
                )
                db.session.add(vehicle1)
                
                vehicle2 = Vehicle(
                    vehicle_number='34나5678',
                    capacity=12,
                    branch_id=branch.id,
                    driver_id=drivers[1].id if len(drivers) > 1 else None
                )
                db.session.add(vehicle2)
                db.session.commit()
                print("✅ 샘플 차량 2대 생성됨 (기사 배정 완료)")
            
            # 샘플 클래스 생성
            if not Class.query.first():
                sample_class = Class(
                    name='아인이수영법1부',
                    branch_id=branch.id if branch else 1,
                    max_students=8,
                    description='초급 수영 클래스'
                )
                db.session.add(sample_class)
                db.session.flush()  # ID 생성
                
                # 클래스 시간대 추가
                time_slot = TimeSlot(
                    class_id=sample_class.id,
                    time='14:00'
                )
                db.session.add(time_slot)
                db.session.commit()
                print("✅ 샘플 클래스 '아인이수영법1부' 생성됨 (14:00)")
            
            print("🎉 초기 데이터 생성 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 초기 데이터 생성 실패: {e}")
            import traceback
            print("📊 상세 오류:")
            traceback.print_exc()
            db.session.rollback()
            return False

def verify_database():
    """데이터베이스 구조 검증"""
    
    with app.app_context():
        try:
            print("\n🔍 데이터베이스 구조 검증 중...")
            
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            # 각 테이블의 컬럼 확인
            tables_to_check = ['branch', 'user', 'class', 'time_slot', 'vehicle', 'student', 'dispatch_result']
            
            for table_name in tables_to_check:
                if table_name in inspector.get_table_names():
                    columns = inspector.get_columns(table_name)
                    print(f"  📋 {table_name} 테이블:")
                    for col in columns:
                        print(f"    - {col['name']}: {col['type']}")
                else:
                    print(f"  ❌ {table_name} 테이블 없음")
            
            # 외래키 관계 확인
            print("\n🔗 외래키 관계 확인:")
            for table_name in inspector.get_table_names():
                fks = inspector.get_foreign_keys(table_name)
                if fks:
                    for fk in fks:
                        print(f"  - {table_name}.{fk['constrained_columns'][0]} → {fk['referred_table']}.{fk['referred_columns'][0]}")
            
            # 데이터 개수 확인
            from models import Branch, User, Vehicle, Class
            print(f"\n📊 데이터 개수:")
            print(f"  - 지점: {Branch.query.count()}개")
            print(f"  - 사용자: {User.query.count()}명")
            print(f"  - 차량: {Vehicle.query.count()}대")
            print(f"  - 클래스: {Class.query.count()}개")
            
            return True
            
        except Exception as e:
            print(f"❌ 검증 실패: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 JOY & POOL 배차 시스템 데이터베이스 초기화")
    print("=" * 60)
    
    # 먼저 models import 확인
    try:
        from models import Branch, User, Class, TimeSlot, Student, Vehicle, DispatchResult
        print("✅ 모든 모델 import 성공")
    except Exception as e:
        print(f"❌ 모델 import 실패: {e}")
        print("app.py의 import 문제를 먼저 해결해주세요!")
        exit(1)
    
    if init_database():
        if create_initial_data():
            if verify_database():
                print("\n🎊 데이터베이스 초기화가 성공적으로 완료되었습니다!")
                print("\n📋 생성된 계정:")
                print("- 마스터 관리자: admin / admin123")
                print("- 지점 관리자: hanam / hanam123") 
                print("- 기사1: driver1 / driver123")
                print("- 기사2: driver2 / driver123")
                print("\n🚗 생성된 차량:")
                print("- 12가3456 (8명, 김기사)")
                print("- 34나5678 (12명, 이기사)")
                print("\n🚀 이제 Flask 애플리케이션을 실행할 수 있습니다!")
                print("   명령어: python app.py")
            else:
                print("\n⚠️ 데이터베이스 검증에 실패했습니다.")
        else:
            print("\n⚠️ 초기 데이터 생성에 실패했습니다.")
    else:
        print("\n❌ 데이터베이스 초기화에 실패했습니다.")