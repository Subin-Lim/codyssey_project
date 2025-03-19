# CSV 파일 읽기 및 리스트 변환
def read_csv(csv_file):
    inventory = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                print("Error: File is empty.")
                return inventory

            headers = lines[0].strip().split(',')
            for line in lines[1:]:
                values = line.strip().split(',')
                if len(values) != len(headers):  # 데이터가 누락된 경우 건너뜀
                    continue
                
                item = {}
                for i in range(len(headers)):
                    try:
                        item[headers[i]] = float(values[i]) if i > 0 else values[i]  # 첫 번째 값(물질명)은 문자열
                    except ValueError:
                        item[headers[i]] = values[i]  # 숫자로 변환 실패 시 문자열 그대로 저장
                
                inventory.append(item)
    except FileNotFoundError:
        print(f'Error: {csv_file} file not found.')
    except Exception as e:
        print(f"Error reading file: {e}")
    return inventory

# 인화성 순으로 정렬 (내림차순)
def sort_by_flammability(inventory):
    return sorted(inventory, key=lambda x: x['Flammability'], reverse=True)

# 인화성 지수 0.7 이상 필터링
def filter_dangerous_items(inventory):
    return [item for item in inventory if item['Flammability'] >= 0.7]

# CSV 파일로 저장
def save_csv(file_name, inventory):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write("Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n")
            for item in inventory:
                file.write(",".join(map(str, item.values())) + "\n")
    except Exception as e:
        print(f"Error writing file: {e}")

# 이진 파일 저장
def save_binary(file_name, inventory):
    try:
        with open(file_name, 'wb') as file:
            for item in inventory:
                line = ",".join(map(str, item.values())) + "\n"
                file.write(line.encode('utf-8'))
    except Exception as e:
        print(f"Error writing binary file: {e}")

# 이진 파일 읽기
def read_binary(file_name):
    try:
        with open(file_name, 'rb') as file:
            content = file.read().decode('utf-8')
            print('\n----------------------------------------------------------------\n')
            print(f'\n{file_name} 내용:')
            print(content)
    except FileNotFoundError:
        print(f'Error: {file_name} file not found.')
    except Exception as e:
        print(f"Error reading binary file: {e}")

def main():
    csv_file = 'Mars_Base_Inventory_List.csv'         
    danger_file_path = 'Mars_Base_Inventory_danger.csv'  
    binary_file_path = 'Mars_Base_Inventory_List.bin'    

    # CSV 파일을 읽어서 리스트로 변환
    inventory = read_csv(csv_file)

    # 원본 파일 내용 출력
    print('\n[Mars_Base_Inventory_List.csv 내용]')
    for item in inventory:
        print(item)

    # 인화성 순으로 정렬
    sorted_inventory = sort_by_flammability(inventory)

    # 인화성 지수 0.7 이상 필터링하여 출력
    dangerous_inventory = filter_dangerous_items(sorted_inventory)
    print('\n----------------------------------------------------------------\n')
    print('\n[인화성 지수 0.7 이상인 목록]')
    for item in dangerous_inventory:
        print(item)

    # CSV 파일 저장
    save_csv(danger_file_path, dangerous_inventory)

    # 이진 파일 저장
    save_binary(binary_file_path, sorted_inventory)

    # 저장된 이진 파일 내용 읽기
    read_binary(binary_file_path)

if __name__ == '__main__':
    main()
