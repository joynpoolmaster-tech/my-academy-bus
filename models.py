# models.py (지점별 권한 분리가 완전히 적용된 버전)
# 기존 models.py 파일을 이 내용으로 완전히 교체하세요.

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from database import db

class Branch(db.Model):
    __tablename__ = 'branch'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    classes = db.relationship('Class', backref='branch', lazy=True, cascade="all, delete-orphan")
    admins = db.relationship('User', backref='managed_branch', foreign_keys='User.branch_id')
    vehicles = db.relationship('Vehicle', backref='branch', lazy=True)
    # 🔹 추가: 학생과 기사 관계
    students = db.relationship('Student', backref='branch', lazy=True)
    drivers = db.relationship('User', backref='driver_branch', foreign_keys='User.driver_branch_id')

    def __repr__(self):
        return f'<Branch {self.name}>'

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 🔹 관리자용 지점 연결
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    
    # 🔹 추가: 기사용 지점 연결 (별도 필드로 분리)
    driver_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=True)
    
    # 관계 설정
    vehicle = db.relationship('Vehicle', backref='driver', uselist=False, foreign_keys='Vehicle.driver_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 🔹 추가: branch_id 필드로 정확한 지점 연결
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    
    # 기존 필드들 (호환성을 위해 유지)
    branch_name = db.Column(db.String(100))
    class_name = db.Column(db.String(100))
    time_slot = db.Column(db.String(50))
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    start_date = db.Column(db.Date)
    emergency_contact = db.Column(db.String(20))
    end_date = db.Column(db.Date)
    extension_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = db.relationship('User', backref=db.backref('student_info', uselist=False))

    def __repr__(self):
        return f'<Student {self.user.name if self.user else "Unknown"}>'

class Class(db.Model):
    __tablename__ = 'class'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    durations = db.Column(db.String(100), nullable=True)  # 쉼표로 구분된 개월 수
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정
    time_slots = db.relationship('TimeSlot', backref='class_ref', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Class {self.name} ({self.branch.name if self.branch else "No Branch"})>'

class TimeSlot(db.Model):
    __tablename__ = 'time_slot'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)  # "08:00~10:00" 또는 "08:00" 형태
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    @property
    def start_time(self):
        """시작 시간만 반환"""
        if '~' in self.time:
            return self.time.split('~')[0]
        return self.time
    
    @property
    def end_time(self):
        """종료 시간만 반환"""
        if '~' in self.time:
            return self.time.split('~')[1]
        return None
    
    @property
    def display_time(self):
        """화면 표시용 시간 형태"""
        if '~' in self.time:
            start, end = self.time.split('~')
            return f"{start} ~ {end}"
        return self.time

    def __repr__(self):
        return f'<TimeSlot {self.time}>'

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # 🔹 수정: nullable=False로 변경하여 모든 차량이 지점에 속하도록 함
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vehicle {self.vehicle_number} (Capacity: {self.capacity})>'

# models.py - DispatchResult 모델 수정

class DispatchResult(db.Model):
    __tablename__ = 'dispatch_results'
    
    id = db.Column(db.Integer, primary_key=True)
    dispatch_date = db.Column(db.Date, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    stop_order = db.Column(db.Integer, default=1)
    
    # 🔹 누락되었던 status 필드 추가
    status = db.Column(db.String(20), default='assigned')  # assigned, in_progress, completed, cancelled
    
    # 🔹 추가 필드들
    pickup_time = db.Column(db.Time, nullable=True)  # 실제 픽업 시간
    arrival_time = db.Column(db.Time, nullable=True)  # 도착 시간
    notes = db.Column(db.Text, nullable=True)  # 특이사항
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    student = db.relationship('Student', backref='dispatch_results', lazy=True)
    vehicle = db.relationship('Vehicle', backref='dispatch_results', lazy=True)
    
    def __repr__(self):
        return f'<DispatchResult {self.id}: {self.dispatch_date}>'
    
    @property
    def status_text(self):
        """상태 텍스트 반환"""
        status_map = {
            'assigned': '배정됨',
            'in_progress': '운행중',
            'completed': '완료',
            'cancelled': '취소됨',
            'pending': '대기중'
        }
        return status_map.get(self.status, '알 수 없음')
    
    def to_dict(self):
        """딕셔너리 형태로 변환"""
        return {
            'id': self.id,
            'dispatch_date': self.dispatch_date.strftime('%Y-%m-%d') if self.dispatch_date else None,
            'student_id': self.student_id,
            'vehicle_id': self.vehicle_id,
            'stop_order': self.stop_order,
            'status': self.status,
            'status_text': self.status_text,
            'pickup_time': self.pickup_time.strftime('%H:%M') if self.pickup_time else None,
            'arrival_time': self.arrival_time.strftime('%H:%M') if self.arrival_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'student_name': self.student.user.name if self.student and self.student.user else None,
            'class_name': self.student.class_name if self.student else None,
            'vehicle_name': self.vehicle.license_plate if self.vehicle else None,
            'driver_name': self.vehicle.driver.name if self.vehicle and self.vehicle.driver else None
        }