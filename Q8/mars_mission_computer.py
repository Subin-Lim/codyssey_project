# import time
# import threading
import platform
import os
import psutil 

"""
class DummySensor:
    def __init__(self):
        self.env_values = {}
        self.set_env()  # 초기 환경 값을 설정

    def set_env(self):
        # 환경 변수 값들을 생성하여 저장
       self.env_values = {
            'mars_base_internal_temperature': round(18.0 + (time.time() % 12), 2),
            'mars_base_external_temperature': round(0 + (time.time() % 21), 2),
            'mars_base_internal_humidity': round(50.0 + (time.time() % 10), 2),
            'mars_base_external_illuminance': round(500.0 + (time.time() % 215), 2),
            'mars_base_internal_co2': round(0.02 + (time.time() % 0.08), 4),
            'mars_base_internal_oxygen': round(4.0 + (time.time() % 3), 2)
        }

    def get_env(self):
        self.set_env() #갱신
        return self.env_values #최신 값 반환
"""

class MissionComputer:
    def __init__(self):
        """ self.sensor = sensor  # 센서 객체
        self.env_values = {}  # 현재 데이터 저장
        self.running = True  # 프로그램 실행 여부
        self.data_log = []  # 5분 동안 수집한 데이터 저장
        self.lock = threading.Lock()  # 데이터 충돌 방지 """
        self.output_fields = self.load_settings()

    """ def get_sensor_data(self):
        print('"s"를 입력하면 출력이 종료됩니다.')
        input_thread = threading.Thread(target=self.input_listener, daemon=True)  # 입력을 감지하는 스레드 실행
        input_thread.start()
        start_time = time.time()

        while self.running:
            self.env_values = self.sensor.get_env()  # 최신 데이터 가져옴
            with self.lock:
                self.data_log.append(self.env_values.copy())  # 데이터 로그에 추가
            self.print_env_values(self.env_values)  # 환경 값 출력
            
            for _ in range(5):  # 5초 동안 입력 확인
                if not self.running:
                    return
                time.sleep(1)
            
            if time.time() - start_time >= 300:  # 5분(300초)마다 평균 출력
                self.print_average()
                start_time = time.time()

    # def input_listener(self):
        # 사용자 입력 감지 및 시스템 종료
        while self.running:
            user_input = input().strip().lower()
            if user_input == 's':  
                self.running = False
                print("System stopped...")

    # def print_env_values(self, env_values):
        # 현재 환경 값을 JSON 형식으로 출력
        print("{")
        for key, value in env_values.items():
            print(f'    "{key}": {value},')
        print("}")

    # def print_average(self):
        # 5분간 수집된 데이터의 평균값 계산 및 출력
        with self.lock:
            if not self.data_log:
                return
            avg_values = {key: sum(d[key] for d in self.data_log) / len(self.data_log) for key in self.data_log[0]}
            self.data_log.clear()  # 데이터 로그 초기화
        print("5분 평균 값:")
        self.print_env_values(avg_values) """

    def load_settings(self):
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print('[경고] setting.txt 파일이 없습니다. 모든 항목을 출력합니다.')
            return []
        
    def get_mission_computer_info(self):
        try:
            info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU 타입': platform.processor(),
                'CPU 코어 수': os.cpu_count(),
                '메모리 크기 (Bytes)': psutil.virtual_memory().total
            }
            print('{')
            for key, value in info.items():
                if not self.output_fields or key in self.output_fields:
                    print(f"    '{key}': '{value}',")
            print('}')
        except Exception as e:
            print('시스템 정보를 가져오는 중 오류가 발생하였습니다.:', e)

    def get_mission_computer_load(self):
        try:
            load = {
                'CPU 실시간 사용량 (%)': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량 (Bytes)': psutil.virtual_memory().used
            }
            print('{')
            for key, value in load.items():
                if not self.output_fields or key in self.output_fields:
                    print(f"    '{key}': {value},")
            print('}')
        except Exception as e:
            print('시스템 부하 정보를 가져오는 중 오류가 발생하였습니다.:', e)

if __name__ == '__main__':
    runComputer = MissionComputer()

    print('=== 미션 컴퓨터 시스템 정보 ===')
    runComputer.get_mission_computer_info()

    print('\n=== 미션 컴퓨터 실시간 부하 정보 ===')
    runComputer.get_mission_computer_load()

    # runComputer.get_sensor_data()

