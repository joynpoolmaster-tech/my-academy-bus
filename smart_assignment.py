# 스마트 기사-차량 배정 시스템
# smart_assignment.py

from flask import Flask
from database import db
from models import *
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
db.init_app(app)

def smart_driver_vehicle_assignment():
    """스마트 기사-차량 배정"""
    
    with app.app_context():
        print("🧠 스마트 기사-차량 배정 시작...")
        
        # 1. 현재 상황 파악
        all_drivers = User.query.filter_by(role='driver').all()
        all_vehicles = Vehicle.query.all()
        
        # 배정된 것들
        assigned_vehicles = [v for v in all_vehicles if v.driver_id is not None]
        assigned_drivers = [d.id for d in all_drivers if any(v.driver_id == d.id for v in all_vehicles)]
        
        # 미배정된 것들
        unassigned_drivers = [d for d in all_drivers if d.id not in assigned_drivers]
        unassigned_vehicles = [v for v in all_vehicles if v.driver_id is None]
        
        print(f"📊 현황:")
        print(f"  전체 기사: {len(all_drivers)}명")
        print(f"  전체 차량: {len(all_vehicles)}대")
        print(f"  배정된 기사: {len(assigned_drivers)}명")
        print(f"  배정된 차량: {len(assigned_vehicles)}대")
        print(f"  미배정 기사: {len(unassigned_drivers)}명")
        print(f"  미배정 차량: {len(unassigned_vehicles)}대")
        
        # 2. 스마트 배정 로직
        if unassigned_drivers and unassigned_vehicles:
            print("\n🔄 자동 배정 중...")
            
            # 지점별 우선 배정
            for driver in unassigned_drivers:
                if not unassigned_vehicles:
                    break
                    
                # 같은 지점 차량 우선 찾기
                same_branch_vehicle = None
                for vehicle in unassigned_vehicles:
                    if (hasattr(driver, 'driver_branch_id') and 
                        hasattr(vehicle, 'branch_id') and
                        driver.driver_branch_id == vehicle.branch_id):
                        same_branch_vehicle = vehicle
                        break
                
                # 배정할 차량 선택
                target_vehicle = same_branch_vehicle or unassigned_vehicles[0]
                
                # 배정 실행
                target_vehicle.driver_id = driver.id
                unassigned_vehicles.remove(target_vehicle)
                
                branch_info = f"(같은지점)" if same_branch_vehicle else f"(다른지점)"
                print(f"  ✅ {driver.name} → {target_vehicle.license_plate} {branch_info}")
            
            db.session.commit()
            print("🎉 자동 배정 완료!")
        
        # 3. 남은 자원 처리 방안 제시
        remaining_drivers = len(unassigned_drivers) - min(len(unassigned_drivers), len(unassigned_vehicles))
        remaining_vehicles = len(unassigned_vehicles) - min(len(unassigned_drivers), len(unassigned_vehicles))
        
        if remaining_drivers > 0:
            print(f"\n⚠️ 남은 기사 {remaining_drivers}명 처리 방안:")
            print("  1. 대기 기사로 운영 (교대, 휴가 대체)")
            print("  2. 차량 추가 구매")
            print("  3. 차량 공유 시스템 (시간대별 교대)")
            
        if remaining_vehicles > 0:
            print(f"\n⚠️ 남은 차량 {remaining_vehicles}대 처리 방안:")
            print("  1. 예비 차량으로 운영 (정비시 대체)")
            print("  2. 기사 추가 채용")
            print("  3. 피크 시간대 추가 운행")
        
        # 4. 배차 시스템 최적화
        print("\n📋 배차 생성 최적화:")
        
        active_pairs = Vehicle.query.filter(Vehicle.driver_id.isnot(None)).all()
        print(f"  활성 기사-차량 조합: {len(active_pairs)}팀")
        
        if active_pairs:
            print("  → 이 조합들로 배차 생성 가능")
            return True
        else:
            print("  → 배차 생성 불가능 (활성 조합 없음)")
            return False

def create_optimized_dispatch():
    """최적화된 배차 생성"""
    
    with app.app_context():
        from datetime import date
        
        today = date.today()
        existing = DispatchResult.query.filter_by(dispatch_date=today).first()
        
        if existing:
            print(f"⚠️ 오늘({today}) 배차가 이미 존재합니다")
            return
        
        # 활성 차량-기사 조합 가져오기
        active_vehicles = Vehicle.query.filter(Vehicle.driver_id.isnot(None)).all()
        available_students = Student.query.limit(10).all()  # 처음 10명
        
        if not active_vehicles:
            print("❌ 활성 차량이 없어 배차 생성 불가")
            return
        
        if not available_students:
            print("❌ 학생이 없어 배차 생성 불가")
            return
        
        print(f"\n🚀 최적화된 배차 생성 중...")
        print(f"  활용 가능 차량: {len(active_vehicles)}대")
        print(f"  대상 학생: {len(available_students)}명")
        
        created_count = 0
        for i, student in enumerate(available_students):
            # 차량 순환 배정 (라운드 로빈)
            vehicle = active_vehicles[i % len(active_vehicles)]
            
            new_dispatch = DispatchResult(
                dispatch_date=today,
                student_id=student.id,
                vehicle_id=vehicle.id,
                stop_order=i + 1,
                status='pending'
            )
            
            db.session.add(new_dispatch)
            created_count += 1
            
            driver_name = User.query.get(vehicle.driver_id).name if vehicle.driver_id else "미지정"
            print(f"  📋 {student.user.name} → {vehicle.license_plate} (기사: {driver_name})")
        
        db.session.commit()
        print(f"✅ 배차 {created_count}건 생성 완료!")

if __name__ == "__main__":
    print("🧠 스마트 기사-차량 배정 시스템")
    print("=" * 40)
    
    # 1. 스마트 배정
    can_dispatch = smart_driver_vehicle_assignment()
    
    # 2. 최적화된 배차 생성
    if can_dispatch:
        create_optimized_dispatch()
    
    print("\n🎯 시스템 최적화 완료!")