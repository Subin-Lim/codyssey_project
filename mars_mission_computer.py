import random

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 20.0,
            'mars_base_external_temperature': 10.0,
            'mars_base_internal_humidity': 55.0,
            'mars_base_external_illuminance': 600.0,
            'mars_base_internal_co2': 0.05,
            'mars_base_internal_oxygen': 5.0
        }
    
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18.0, 30.0), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0.0, 21.0), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50.0, 60.0), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500.0, 715.0), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        current_time = "2025-03-27 08:30:00"  
        log_data = (
            f'{current_time} \n'
            f"화성 기지 내부 온도: {self.env_values['mars_base_internal_temperature']} 도\n"
            f"화성 기지 외부 온도: {self.env_values['mars_base_external_temperature']} 도\n"
            f"화성 기지 내부 습도: {self.env_values['mars_base_internal_humidity']} %\n"
            f"화성 기지 외부 광량: {self.env_values['mars_base_external_illuminance']} W/m²\n"
            f"화성 기지 내부 CO2 농도: {self.env_values['mars_base_internal_co2']} %\n"
            f"화성 기지 내부 산소 농도: {self.env_values['mars_base_internal_oxygen']} %\n"
            f'--------------------------------------------------\n'
        )

        with open('sensor_log.log', 'a', encoding='utf-8') as file:
            file.write(log_data)

        return self.env_values

if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()  
    env_data = ds.get_env()  

    print('[더미 센서 값 출력]')
    for key, value in env_data.items():
        if 'temperature' in key:
            print(f'{key}: {value} 도')
        elif 'humidity' in key or 'oxygen' in key:
            print(f'{key}: {value} %')
        elif 'illuminance' in key:
            print(f'{key}: {value} W/m²')
        elif 'co2' in key:
            print(f'{key}: {value} %')
