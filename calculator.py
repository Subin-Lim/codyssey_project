import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('계산기')       
        self.setFixedSize(300, 500)        
        self.expression = ''                
        self.init_ui()                      

    # UI 구성 함수
    def init_ui(self):
        self.setStyleSheet('background-color: black;')  
        self.display = QLabel('0')                     
        self.display.setStyleSheet('font-size: 30px; background-color: black; color: white; padding: 10px;')
        self.display.setFixedHeight(60)                 
        self.display.setAlignment(Qt.AlignRight)       

        layout = QVBoxLayout()                         
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(self.display)                 

        grid_layout = QGridLayout()                    

        # 버튼 텍스트 배열 (행, 열 순서)
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+']
        ]

        # 일반 버튼들 생성
        for row_idx, row in enumerate(buttons):
            for col_idx, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.setFixedSize(60, 60)

                # 버튼 스타일 지정 (색 구분)
                if button_text in ['÷', '×', '-', '+']:
                    style = 'font-size: 20px; color: white; background-color: #f57c00; border: none;'
                elif button_text in ['AC', '±', '%']:
                    style = 'font-size: 20px; color: black; background-color: #a5a5a5; border: none;'
                else:
                    style = 'font-size: 20px; color: white; background-color: #333; border: none;'

                button.setStyleSheet(style)
                button.clicked.connect(self.on_button_click)  
                grid_layout.addWidget(button, row_idx + 1, col_idx)  

        zero_button = QPushButton('0')
        zero_button.setFixedSize(60 * 2 + 10, 60)
        zero_button.setStyleSheet(
            'font-size: 20px; color: white; background-color: #333; border: none; text-align: left; padding-left: 15px;'
        )
        zero_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(zero_button, 5, 0, 1, 2)

        dot_button = QPushButton('.')
        dot_button.setFixedSize(60, 60)
        dot_button.setStyleSheet('font-size: 20px; color: white; background-color: #333; border: none;')
        dot_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(dot_button, 5, 2)


        equal_button = QPushButton('=')
        equal_button.setFixedSize(60, 60)
        equal_button.setStyleSheet('font-size: 20px; color: white; background-color: #f57c00; border: none;')
        equal_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(equal_button, 5, 3)

        layout.addLayout(grid_layout)
        self.setLayout(layout)  

    # 버튼 클릭 시 실행되는 함수
    def on_button_click(self):
        button = self.sender()         # 어떤 버튼을 눌렀는지 가져오기
        text = button.text()          # 버튼에 적힌 글자

        if text == 'AC':
            self.display.setText('0')  # 초기화
            self.expression = ''

        elif text == '=':
            try:
                result = eval(self.expression)

                # 소수점 없는 float → 정수로 변환 
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)  # 결과를 expression에 저장
                self.display.setText("{:,}".format(result))  # 쉼표 넣어서 출력
            except Exception:
                self.display.setText('Error')
                self.expression = ''

        elif text in ['+', '-', '×', '÷']:
            if text == '×':
                self.expression += '*'
            elif text == '÷':
                self.expression += '/'
            else:
                self.expression += text

            self.display.setText(self.display.text() + text)

        elif text.isdigit() or text == '.':
            if self.display.text() in ['0', 'Error']:
                self.expression = text
            else:
                self.expression += text

            tokens = re.split(r'([+\-*/])', self.expression)
            formatted = ''
            for i, tok in enumerate(tokens):
                if i % 2 == 0:  # 숫자일 때
                    if tok:
                        if '.' in tok:
                            integer_part, decimal_part = tok.split('.')
                            formatted += "{:,}".format(int(integer_part)) + '.' + decimal_part
                        else:
                            formatted += "{:,}".format(int(tok))
                else:  
                    formatted += tok
            self.display.setText(formatted)

        else:
            pass


# 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)  
    calculator = Calculator()     
    calculator.show()            
    sys.exit(app.exec_())         
