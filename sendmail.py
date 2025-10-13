import smtplib
import ssl
from email.message import EmailMessage
import os


def create_email(sender, recipient, subject, body, attachment_path=None):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.set_content(body)

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as file:
                file_data = file.read()
                file_name = os.path.basename(attachment_path)
                message.add_attachment(
                    file_data,
                    maintype='application',
                    subtype='octet-stream',
                    filename=file_name
                )
        except FileNotFoundError:
            print('첨부 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.')
        except Exception as e:
            print('첨부 파일 처리 중 오류 발생:', str(e))

    return message


def send_email(sender, password, recipient, subject, body, attachment_path=None):
    message = create_email(sender, recipient, subject, body, attachment_path)
    smtp_server = 'smtp.gmail.com'
    port = 587  # TLS 포트

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender, password)
            server.send_message(message)
            print('이메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('인증에 실패했습니다. 이메일 주소와 비밀번호(앱 비밀번호)를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('SMTP 서버에 연결할 수 없습니다.')
    except smtplib.SMTPException as e:
        print('SMTP 오류 발생:', str(e))
    except Exception as e:
        print('알 수 없는 오류 발생:', str(e))


if __name__ == '__main__':
    # 사용자 입력 부분
    sender_email = 'binisu49@gmail.com'  # 본인 Gmail 계정
    sender_password = 'duog libe cvpn wwrp'  # 앱 비밀번호 사용 (2단계 인증 필요)
    recipient_email = 'binisu49@naver.com'  # 받을 사람 이메일
    email_subject = '파이썬 이메일 전송 테스트'
    email_body = '안녕하세요, 파이썬으로 보낸 메일입니다.'
    attachment_file = None  # 예: 'test.txt' 또는 None

    send_email(
        sender_email,
        sender_password,
        recipient_email,
        email_subject,
        email_body,
        attachment_file
    )
