# chat_server.py
import socket
import threading

# 접속된 클라이언트를 관리하는 리스트
clients = []

def handle_client(client_socket):
    """
    개별 클라이언트의 메시지를 처리하는 함수
    """
    try:
        # 클라이언트 IP 주소와 포트 번호
        ip_port = client_socket.getpeername()
        client_address = f'{ip_port[0]}:{ip_port[1]}'
        print(f'[+] {client_address} 님이 입장하셨습니다.')

        # 입장 메시지를 모든 클라이언트에게 전송
        entry_message = f'📢 {client_address} 님이 입장하셨습니다.'
        broadcast(entry_message.encode('utf-8'))

        while True:
            # 클라이언트로부터 데이터 수신
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            
            # 클라이언트가 '/종료'를 입력하면 연결 종료
            if message.strip() == '/종료':
                break

            # 귓속말 기능 처리
            if message.startswith('/귓속말'):
                try:
                    parts = message.split(' ', 2)
                    target_address = parts[1]
                    private_message = parts[2]
                    send_private_message(client_address, target_address, private_message)
                except IndexError:
                    pass  # 잘못된 귓속말 형식은 무시
                continue

            # 일반 메시지 전체 전송
            full_message = f'{client_address}> {message}'
            print(full_message)
            broadcast(full_message.encode('utf-8'))

    except (ConnectionResetError, BrokenPipeError):
        # 연결이 강제로 끊어졌을 때의 예외 처리
        pass
    finally:
        # 연결이 끊어졌을 때 클라이언트 리스트에서 제거
        if client_socket in clients:
            clients.remove(client_socket)
        
        print(f'[-] {client_address} 님이 퇴장하셨습니다.')
        exit_message = f'📢 {client_address} 님이 퇴장하셨습니다.'
        broadcast(exit_message.encode('utf-8'))
        client_socket.close()

def broadcast(message):
    """
    모든 접속된 클라이언트에게 메시지를 전송하는 함수
    """
    for client in clients:
        try:
            client.send(message)
        except (BrokenPipeError, ConnectionResetError):
            # 연결이 끊긴 클라이언트는 예외 처리
            pass

def send_private_message(sender_address, target_address, message):
    """
    특정 클라이언트에게만 메시지를 전송하는 귓속말 기능
    """
    found = False
    for client in clients:
        ip_port = client.getpeername()
        client_address = f'{ip_port[0]}:{ip_port[1]}'
        if client_address == target_address:
            private_message = f'[귓속말] {sender_address}> {message}'
            try:
                client.send(private_message.encode('utf-8'))
                found = True
                print(f'[귓속말] {sender_address} -> {target_address}: {message}')
            except (BrokenPipeError, ConnectionResetError):
                pass
            break
    
    # 보낸 사람에게는 성공 여부 알림
    for client in clients:
        ip_port = client.getpeername()
        client_address = f'{ip_port[0]}:{ip_port[1]}'
        if client_address == sender_address:
            status_message = ''
            if found:
                status_message = f'[귓속말] {target_address} 에게 메시지를 보냈습니다.'
            else:
                status_message = f'[귓속말] {target_address} 님을 찾을 수 없습니다.'
            try:
                client.send(status_message.encode('utf-8'))
            except (BrokenPipeError, ConnectionResetError):
                pass
            break

def main():
    """
    서버를 실행하고 클라이언트 연결을 수락하는 메인 함수
    """
    host = '0.0.0.0'
    port = 5555
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    
    print(f'[+] 서버가 {host}:{port} 에서 대기 중입니다...')
    
    while True:
        client_socket, addr = server.accept()
        print(f'[+] 연결 수락: {addr}')
        
        # 접속한 클라이언트를 리스트에 추가
        clients.append(client_socket)
        
        # 클라이언트별로 새로운 쓰레드 생성
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()