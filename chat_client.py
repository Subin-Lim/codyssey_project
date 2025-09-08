# chat_client.py
import socket
import threading
import sys

def receive_messages(sock):
    """
    서버로부터 메시지를 수신하는 함수
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print('서버와 연결이 끊어졌습니다.')
                break
            # UTF-8로 디코딩 후 출력
            print(data.decode('utf-8'))
        except (ConnectionResetError, BrokenPipeError):
            print('서버와 연결이 끊어졌습니다.')
            break
        except Exception as e:
            print(f'오류 발생: {e}')
            break

def main():
    """
    클라이언트를 실행하고 서버에 연결하는 메인 함수
    """
    host = '127.0.0.1'  # 서버 주소 (서버가 실행 중인 컴퓨터의 IP)
    port = 5555         # 서버 포트 번호
    
    # TCP/IP 소켓 생성
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 서버에 연결
        client.connect((host, port))
        print('서버에 연결되었습니다. 메시지를 입력하세요.')
        print('종료하려면 "/종료"를 입력하세요.')
    except ConnectionRefusedError:
        print('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')
        sys.exit()
    
    # 서버로부터 메시지를 받기 위한 별도의 쓰레드 생성
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True # 메인 쓰레드 종료 시 함께 종료되도록 설정
    receive_thread.start()
    
    # 사용자 입력 루프
    while True:
        message = input('')
        
        # 메시지 인코딩 후 서버로 전송
        client.send(message.encode('utf-8'))
        
        # '/종료' 입력 시 클라이언트 종료
        if message == '/종료':
            break
            
    # 소켓 닫기
    client.close()

if __name__ == '__main__':
    main()