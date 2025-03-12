print('Hello Mars')

def read_log(log_file):
    try:
        f = open(log_file, 'r', encoding='utf-8') 
        file = f.readlines()
        for line in file:
            print(line.strip())  
    except FileNotFoundError:
        print(f'오류: {log_file} 파일을 찾을 수 없습니다.')
    except Exception as error:
        print(f'오류 발생: {error}')


def read_log_reversed(log_file):
    try:
        f = open(log_file, 'r', encoding='utf-8') 
        file = f.readlines()
        for line in reversed(file):
            print(line.strip())
    except FileNotFoundError:
        print(f'오류: {log_file} 파일을 찾을 수 없습니다.')
    except Exception as error:
        print(f'오류 발생: {error}')

log_filename = 'mission_computer_main.log'
read_log(log_filename)
read_log_reversed(log_filename)