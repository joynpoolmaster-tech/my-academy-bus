<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>관리자 - 기사/차량 관리</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans KR', sans-serif; }
        .admin-sidebar-bg { background-color: #F0F9FF; }
        .admin-header-bg { background-color: #E0F2FE; }
    </style>
</head>
<body class="bg-gray-100 flex">

    <!-- 사이드바 -->
    <div class="admin-sidebar-bg w-64 min-h-screen p-4 hidden md:block">
        <div class="text-2xl font-bold text-blue-800 mb-8">배차 관리 시스템</div>
        <nav class="space-y-2">
            <!-- 마스터 전용 메뉴 -->
            {% if session.get('role') == 'master' %}
            <a href="{{ url_for('manage_branches') }}" 
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-blue-100">
                지점/관리자 관리
            </a>
            {% endif %}

            <!-- 관리자 공용 메뉴 -->
            <a href="{{ url_for('admin_dashboard') }}" 
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-blue-100">
                대시보드
            </a>
            <a href="{{ url_for('manage_students') }}" 
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-blue-100">
                회원 관리
            </a>
            <a href="{{ url_for('manage_classes') }}" 
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-blue-100">
                클래스 관리
            </a>
            <a href="{{ url_for('manage_vehicles') }}" 
               class="flex items-center p-3 rounded-lg text-blue-900 bg-blue-200 font-bold">
                기사/차량 관리
            </a>
            <a href="{{ url_for('manage_dispatch') }}" 
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-blue-100">
                배차 관리
            </a>
        </nav>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="flex-1 flex flex-col">
        <header class="admin-header-bg p-4 flex justify-between items-center shadow-md">
            <h2 class="text-xl font-bold text-blue-800">기사 및 차량 관리</h2>
            <div>
                <span class="mr-4">{{ session.get('user_name') }}님</span>
                <a href="{{ url_for('logout') }}" class="bg-white text-blue-600 px-4 py-2 rounded-lg shadow hover:bg-gray-100">로그아웃</a>
            </div>
        </header>
        
        <main class="flex-1 p-6">
            <!-- Flash 메시지 표시 -->
            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="mb-4 p-4 rounded-md 
                    {% if category == 'success' %} bg-green-100 text-green-700 
                    {% elif category == 'danger' %} bg-red-100 text-red-700 
                    {% elif category == 'warning' %} bg-yellow-100 text-yellow-700
                    {% else %} bg-blue-100 text-blue-700 {% endif %}"
                    role="alert">
                    {{ message }}
                  </div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 새 기사/차량 추가 카드 -->
                <div class="lg:col-span-1 space-y-6">
                    <!-- 새 기사 계정 생성 -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">새 기사 계정 생성</h3>
                        <form method="POST" action="{{ url_for('add_driver') }}" class="space-y-4">
                            <div>
                                <label for="driver_name" class="block text-sm font-medium text-gray-700">이름</label>
                                <input type="text" name="name" id="driver_name" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <div>
                                <label for="driver_email" class="block text-sm font-medium text-gray-700">이메일 (로그인 ID)</label>
                                <input type="email" name="email" id="driver_email" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <div>
                                <label for="driver_phone" class="block text-sm font-medium text-gray-700">연락처</label>
                                <input type="text" name="phone" id="driver_phone" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <div>
                                <label for="driver_password" class="block text-sm font-medium text-gray-700">초기 비밀번호</label>
                                <input type="password" name="password" id="driver_password" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">기사 생성</button>
                        </form>
                    </div>
                    <!-- 새 차량 등록 -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">새 차량 등록</h3>
                        <form method="POST" action="{{ url_for('add_vehicle') }}" class="space-y-4">
                            <div>
                                <label for="vehicle_number" class="block text-sm font-medium text-gray-700">차량 이름 (예: 1호차)</label>
                                <input type="text" name="vehicle_number" id="vehicle_number" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <div>
                                <label for="capacity" class="block text-sm font-medium text-gray-700">정원 (숫자만)</label>
                                <input type="number" name="capacity" id="capacity" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm" required>
                            </div>
                            <button type="submit" class="w-full bg-green-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700">차량 등록</button>
                        </form>
                    </div>
                </div>

                <!-- 현재 차량 목록 및 기사 배정 -->
                <div class="lg:col-span-2 bg-white p-6 rounded-lg shadow-md">
                    <h3 class="font-bold text-lg mb-4">차량 목록 및 기사 배정</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left">
                            <thead>
                                <tr class="border-b bg-gray-50">
                                    <th class="py-3 px-4">차량</th>
                                    <th class="py-3 px-4">정원</th>
                                    <th class="py-3 px-4">담당 기사</th>
                                    <th class="py-3 px-4">작업</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for vehicle in vehicles %}
                                <tr class="border-b">
                                    <td class="py-3 px-4 font-bold">{{ vehicle.vehicle_number }}</td>
                                    <td class="py-3 px-4">{{ vehicle.capacity }}명</td>
                                    <td class="py-3 px-4">
                                        <form method="POST" action="{{ url_for('assign_driver', vehicle_id=vehicle.id) }}">
                                            <select name="driver_id" class="border-gray-300 rounded-md shadow-sm">
                                                <option value="0">-- 기사 선택 --</option>
                                                {% for driver in drivers %}
                                                <option value="{{ driver.id }}" {% if vehicle.driver_id == driver.id %}selected{% endif %}>
                                                    {{ driver.name }} ({{ driver.phone }})
                                                </option>
                                                {% endfor %}
                                            </select>
                                            <button type="submit" class="ml-2 bg-gray-500 text-white px-3 py-1 text-sm rounded-md hover:bg-gray-600">배정</button>
                                        </form>
                                    </td>
                                    <td class="py-3 px-4">
                                        <form method="POST" action="{{ url_for('delete_vehicle', vehicle_id=vehicle.id) }}">
                                            <button type="submit" class="text-red-500 hover:text-red-700 text-xs">차량삭제</button>
                                        </form>
                                    </td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="4" class="text-center py-10 text-gray-500">등록된 차량이 없습니다.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    </div>

</body>
</html>