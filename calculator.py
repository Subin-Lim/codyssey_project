import sys
import re 
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QFont
import traceback 


class Calculator(QWidget):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('계산기') 
        self.setFixedSize(300, 500) 
        self.expression = ''
        self.last_was_equal = False 
        self.init_ui() 

    def init_ui(self):
        self.setStyleSheet('background-color: black;') 

        self.display = QLabel('0')
        self.display.setStyleSheet('font-size: 30px; background-color: black; color: white; padding: 10px;')
        self.display.setFixedHeight(60)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 

        # 폰트 크기 자동 조절을 위한 초기 설정
        self.initial_font_size = 30 # 초기 폰트 크기
        self.min_font_size = 10 # 최소 폰트 크기
        self.base_display_style = 'background-color: black; color: white; padding: 10px;' 

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(self.display) 

    
        grid_layout = QGridLayout()
        # 버튼 텍스트 정의
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, button_text in enumerate(row):
                button = QPushButton(button_text)
                button.setFixedSize(60, 60)

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
        zero_button.setFixedSize(130, 60)
        zero_button.setStyleSheet('font-size: 20px; color: white; background-color: #333; border: none; text-align: left; padding-left: 15px;')
        zero_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(zero_button, 5, 0, 1, 2) 

        # 소수점 . 버튼
        dot_button = QPushButton('.')
        dot_button.setFixedSize(60, 60)
        dot_button.setStyleSheet('font-size: 20px; color: white; background-color: #333; border: none;')
        dot_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(dot_button, 5, 2)

        # 등호 = 버튼
        equal_button = QPushButton('=')
        equal_button.setFixedSize(60, 60)
        equal_button.setStyleSheet('font-size: 20px; color: white; background-color: #f57c00; border: none;')
        equal_button.clicked.connect(self.on_button_click)
        grid_layout.addWidget(equal_button, 5, 3)

        layout.addLayout(grid_layout) 
        self.setLayout(layout) 

        # 초기 폰트 크기 조절 실행
        self.adjust_display_font_size()

    # 계산 결과 출력 값 길이에 따라 폰트 크기 자동 조절
    def adjust_display_font_size(self):
        text = self.display.text()
        if not text:
            return

        # 디스플레이 라벨의 실제 사용 가능한 너비 계산 
        available_width = self.display.width() - self.display.contentsMargins().left() - self.display.contentsMargins().right()

        if available_width <= 0:
            return

        test_font = QFont(self.display.font()) # 폰트 복사
        # 초기 크기부터 최소 크기까지 줄여가며 테스트
        for size in range(self.initial_font_size, self.min_font_size - 1, -1):
            test_font.setPixelSize(size) # 테스트할 폰트 크기 설정
            metrics = QFontMetrics(test_font) 
            text_width = metrics.horizontalAdvance(text) 

            if text_width <= available_width: # 측정된 텍스트 너비가 사용 가능 너비 이하면
                # 해당 폰트 크기로 스타일 설정하고 메소드 종료
                self.display.setStyleSheet(f'font-size: {size}px; {self.base_display_style}')
                return

        # 최소 크기로도 다 표시 못하면 최소 크기로 설정
        self.display.setStyleSheet(f'font-size: {self.min_font_size}px; {self.base_display_style}')


    def format_input_segment(self, segment_str):
        if not segment_str:
            return ''

        # 음수 부호 처리
        is_negative = segment_str.startswith('-')
        if is_negative:
            number_part = segment_str[1:]
        else:
            number_part = segment_str

        # 특수 입력 처리: '-'만 있거나 '.'만 있는 경우
        if number_part == '': # '-'만 있는 경우
             return '-' if is_negative else ''
        if number_part == '.': # '.'만 있는 경우 ('-.' 포함) -> '0.' 또는 '-0.'으로 표시
             return '-0.' if is_negative else '0.'

        parts = number_part.split('.', 1)
        integer_part_str = parts[0]
        decimal_part_str = parts[1] if len(parts) > 1 else ''
        has_explicit_decimal_point = '.' in number_part 

        formatted_integer_part = ''
        if integer_part_str:
             try:
                 formatted_integer_part = f"{int(integer_part_str):,}" # 3자리마다 쉼표 추가
             except ValueError:
                  formatted_integer_part = integer_part_str

        formatted_segment = formatted_integer_part

        if has_explicit_decimal_point:
             formatted_segment += '.' + decimal_part_str

        if is_negative:
             formatted_segment = '-' + formatted_segment

        if segment_str == '-0' and not has_explicit_decimal_point:
             formatted_segment = '0'
        elif segment_str == '0' and not formatted_segment: 
             formatted_segment = '0'

        return formatted_segment

    # 현재 계산식을 디스플레이에 표시되도록 업데이트
    def update_display_text(self):
        """현재 표현식 문자열에 기반하여 디스플레이 QLabel을 업데이트하고 숫자 부분을 포맷합니다."""
        if not self.expression:
            self.display.setText('0') # 표현식이 비었으면 초기값 '0' 표시
            self.adjust_display_font_size() 
            return

        parts_and_operators = re.split(r'([+\-×÷])', self.expression) 

        display_parts = [] 
        i = 0 
        while i < len(parts_and_operators):
             part = parts_and_operators[i]

             if part in '+-×÷': 
                 display_parts.append(part)
                 i += 1
             elif part != '': 
                  if part == '-' and i > 0 and parts_and_operators[i-1] in '+-×÷':
                       if i + 1 < len(parts_and_operators) and parts_and_operators[i+1] != '' and parts_and_operators[i+1] not in '+-×÷':
                            number_segment_str = '-' + parts_and_operators[i+1] 
                            formatted_part = self.format_input_segment(number_segment_str) 
                            display_parts.append(formatted_part) 
                            i += 2 
                       else:
                            display_parts.append(part)
                            i += 1
                  elif part == '-' and i == 0: 
                       if i + 1 < len(parts_and_operators) and parts_and_operators[i+1] != '' and parts_and_operators[i+1] not in '+-×÷':
                            number_segment_str = '-' + parts_and_operators[i+1] 
                            formatted_part = self.format_input_segment(number_segment_str) 
                            display_parts.append(formatted_part) 
                            i += 2
                       else:
                            display_parts.append(part)
                            i += 1

                  else: 
                      formatted_part = self.format_input_segment(part) 
                      display_parts.append(formatted_part) 
                      i += 1
             else: 
                  i += 1

        display_text = ''.join(display_parts)

        if not display_text and self.expression:
             if self.expression == '-': display_text = '-'
             elif self.expression == '.': display_text = '0.'
             elif re.fullmatch(r'^-?(\d*\.?\d*|\.\d*)$', self.expression): 
                 display_text = self.format_input_segment(self.expression)
             else: display_text = self.expression 

        if not display_text and not self.expression:
             display_text = '0'

        self.display.setText(display_text) 
        self.adjust_display_font_size()

    def tokenize_and_process(self, expression_str):
        if not expression_str:
            return []

        raw_tokens = re.findall(r'\d*\.?\d+|\.\d+|[+\-×÷]', expression_str)

        processed_tokens = [] 
        i = 0 
        while i < len(raw_tokens):
            token = raw_tokens[i]

            if token == '-':
                if not processed_tokens or isinstance(processed_tokens[-1], str):
                    if i + 1 < len(raw_tokens) and re.fullmatch(r'\d*\.?\d+|\.\d+', raw_tokens[i+1]): 
                        number_str = '-' + raw_tokens[i+1] 
                        try:
                            processed_tokens.append(float(number_str)) 
                            i += 2 
                        except ValueError: 
                             raise ValueError("잘못된 숫자 형식")
                    else:
                        raise ValueError("잘못된 표현식") 
                else:
                    processed_tokens.append(token)
                    i += 1
            elif token in '+×÷': 
                processed_tokens.append(token) 
                i += 1 
            elif re.fullmatch(r'\d*\.?\d+|\.\d+', token): 
                if processed_tokens and isinstance(processed_tokens[-1], (int, float)):
                     raise ValueError("잘못된 표현식") 

                try:
                    processed_tokens.append(float(token)) 
                    i += 1 
                except ValueError: 
                     raise ValueError("잘못된 숫자 형식") 
            else: 
                raise ValueError(f"알 수 없는 토큰: {token}") 

        if processed_tokens and isinstance(processed_tokens[-1], str):
             pass

        return processed_tokens 

    # AC 버튼
    def reset(self):
        self.expression = ''
        self.last_was_equal = False
        self.update_display_text()

    # ± 버튼
    def negative_positive(self):
        if self.display.text() in ['0', 'Error', '0으로 나눌 수 없습니다', 'N/A']:
             return

        match = re.search(r'([+\-×÷])?(-?\d+\.?\d*|\.\d+)$', self.expression)

        if match: # 마지막이 숫자로 끝나는 경우
             preceding_operator = match.group(1) or ''
             number_str = match.group(2) 
             start_index_of_number = match.start(2) 

             if number_str == '.' or number_str == '': 
                  return

             try:
                  current_value = float(number_str) 
                  new_value = -current_value # 부호 반전
                  new_number_str = str(new_value) 

                  self.expression = self.expression[:start_index_of_number] + new_number_str

                  self.update_display_text()
                  self.last_was_equal = False

             except ValueError: 
                  self.display.setText('Error')
                  self.expression = ''
                  self.last_was_equal = False
                  self.adjust_display_font_size()

    # 퍼센트 계산 (%)
    def percent(self):
        if self.display.text() in ['0', 'Error', '0으로 나눌 수 없습니다', 'N/A']:
             return

        match = re.search(r'(-?\d+\.?\d*|\.\d+)$', self.expression)

        if match: # 마지막이 숫자로 끝나는 경우
             number_str = match.group(0)
             start_index = match.start(0)

             if number_str == '.' or number_str == '':
                  return

             try:
                  current_value = float(number_str) 
                  new_value = current_value / 100.0 # 100으로 나누기 (퍼센트)
                  new_number_str = str(new_value) 

                  self.expression = self.expression[:start_index] + new_number_str

                  self.update_display_text()
                  self.last_was_equal = False

             except ValueError:
                  self.display.setText('Error') 
                  self.expression = ''
                  self.last_was_equal = False
                  self.adjust_display_font_size()
             except ZeroDivisionError: 
                  self.display.setText('Error')
                  self.expression = ''
                  self.last_was_equal = False
                  self.adjust_display_font_size()

    # 숫자 버튼 처리 (0-9)
    def handle_digit(self, digit):
        if self.last_was_equal or self.display.text() in ['Error', '0으로 나눌 수 없습니다', 'N/A']:
            self.expression = digit 
        else:
            # "-" 뒤에 "0" 오는 경우 허용 ("-0" 가능)
            if self.expression == '-' and digit == '0':
                 self.expression += digit
            else:
                 last_operator_index = max([self.expression.rfind(op) for op in '+-×÷'] + [-1]) 
                 last_segment = self.expression[last_operator_index + 1:]

                 if last_segment == '0' and digit == '0' and '.' not in last_segment:
                      pass 
                 elif last_segment == '0' and digit != '0' and '.' not in last_segment:
                      self.expression = self.expression[:last_operator_index + 1] + digit 
                 else:
                      self.expression += digit

        self.last_was_equal = False 
        self.update_display_text() 

    # 소수점 버튼 처리 (.)
    def handle_decimal(self):
        if self.last_was_equal or self.display.text() in ['Error', '0으로 나눌 수 없습니다', 'N/A']:
            self.expression = '0.' 
        else:
            last_operator_index = max([self.expression.rfind(op) for op in '+-×÷'] + [-1]) 
            last_segment = self.expression[last_operator_index + 1:]

            # 제약사항: 소수점 중복 방지
            if '.' not in last_segment: 
                if last_segment == '': 
                    self.expression += '0.'
                elif last_segment == '-': 
                    self.expression += '.'
                else: 
                    self.expression += '.'

        self.last_was_equal = False 
        self.update_display_text() 

    # 연산자 버튼 처리 (+, -, ×, ÷)
    def handle_operator(self, operator):
        if not self.expression and operator != '-':
             return

        if self.last_was_equal:
            if self.display.text() in ['Error', '0으로 나눌 수 없습니다', 'N/A']:
                return
            self.expression = self.expression + operator 
            self.last_was_equal = False 
        else:
            if self.expression and self.expression[-1] in '+-×÷':
                 if self.expression[-1] == '-' and operator == '-':
                     self.expression += operator
                 elif self.expression[-1] in '+×÷' and operator == '-':
                     self.expression += operator
                 else:
                      self.expression = self.expression[:-1] + operator
            else: 
                self.expression += operator

        self.update_display_text() 

    # 사칙 연산 메소드
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다") 
        return a / b 

    # 계산 실행 (등호 버튼)
    def equal(self):
        if self.last_was_equal or self.display.text() in ['Error', '0으로 나눌 수 없습니다', 'N/A']:
            return

        calculation_expression = self.expression.strip()

        if calculation_expression and calculation_expression[-1] in '+×÷':
             calculation_expression = calculation_expression[:-1]
        elif calculation_expression.endswith('-') and len(calculation_expression) > 1:
             if calculation_expression[-2] in '+-×÷':
                 calculation_expression = calculation_expression[:-1]

        if not calculation_expression or calculation_expression == '-':
             self.display.setText('0')
             self.expression = ''
             self.last_was_equal = False
             self.adjust_display_font_size()
             return

        try:
            calculation_list = self.tokenize_and_process(calculation_expression)

            if not calculation_list: 
                 raise ValueError("유효한 표현식이 없습니다.") 
            
            i = 0
            while i < len(calculation_list):
                if calculation_list[i] in ['×', '÷']: 
                    if i == 0 or i >= len(calculation_list) - 1 or \
                       not isinstance(calculation_list[i-1], (int, float)) or \
                       not isinstance(calculation_list[i+1], (int, float)):
                         raise ValueError(f"유효하지 않은 연산 순서: {calculation_list[i]} 연산") 

                    try:
                        operand1 = calculation_list[i-1]
                        operand2 = calculation_list[i+1]
                        operator = calculation_list[i]

                        if operator == '×': result = self.multiply(operand1, operand2)
                        elif operator == '÷': result = self.divide(operand1, operand2) 

                        calculation_list[i-1:i+2] = [result]
                        i -= 1 

                    except (ValueError, TypeError, IndexError) as e: 
                        raise ValueError(f"계산 중 오류 발생 ({e})") 
                else:
                     i += 1 

            i = 0 
            while i < len(calculation_list):
                 if calculation_list[i] in ['+', '-']: 
                      if i == 0 or i >= len(calculation_list) - 1 or \
                         not isinstance(calculation_list[i-1], (int, float)) or \
                         not isinstance(calculation_list[i+1], (int, float)):
                           raise ValueError(f"유효하지 않은 연산 순서: {calculation_list[i]} 연산") 
                      try:
                           operand1 = calculation_list[i-1]
                           operand2 = calculation_list[i+1]
                           operator = calculation_list[i]

                           if operator == '+': result = self.add(operand1, operand2)
                           elif operator == '-': result = self.subtract(operand1, operand2)

                           calculation_list[i-1:i+2] = [result]
                           i -= 1

                      except (ValueError, TypeError, IndexError) as e:
                           raise ValueError(f"계산 중 오류 발생 ({e})") 
                 else:
                      i += 1 

            if len(calculation_list) != 1 or not isinstance(calculation_list[0], (int, float)):
                 raise ValueError("계산 결과 오류: 표현식 형식 오류") 

            final_result = calculation_list[0] 

            if not (float('-inf') < final_result < float('inf')):
                 self.display.setText("N/A") 
                 self.expression = ''
                 self.last_was_equal = False
                 self.adjust_display_font_size()
                 return

            result_str_check = str(final_result) 
            if 'e' in result_str_check: 
                 try:
                      exponent = float(result_str_check.split('e')[-1])
                      if abs(exponent) > 15: 
                           self.display.setText("N/A")
                           self.expression = ''
                           self.last_was_equal = False
                           self.adjust_display_font_size()
                           return
                 except (ValueError, IndexError):
                      self.display.setText("N/A")
                      self.expression = ''
                      self.last_was_equal = False
                      self.adjust_display_font_size()
                      return
            # 소수점이 있거나 음수 정수거나 양수 정수인 경우 정수부 길이 체크 (15자리 초과 시 N/A)
            elif '.' in result_str_check:
                 integer_part_str = result_str_check.split('.')[0].lstrip('-')
                 if len(integer_part_str) > 15:
                     self.display.setText("N/A")
                     self.expression = ''
                     self.last_was_equal = False
                     self.adjust_display_font_size()
                     return
            elif result_str_check.startswith('-'):
                 if len(result_str_check[1:]) > 15:
                       self.display.setText("N/A")
                       self.expression = ''
                       self.last_was_equal = False
                       self.adjust_display_font_size()
                       return
            elif len(result_str_check) > 15:
                 self.display.setText("N/A")
                 self.expression = ''
                 self.last_was_equal = False
                 self.adjust_display_font_size()
                 return

            self.expression = str(final_result) 

            # 소수점 6자리 이하 반올림 
            formatted_result_display = self.format_number(final_result)
            self.display.setText(formatted_result_display) 

            self.last_was_equal = True 
            self.adjust_display_font_size() 

        except ZeroDivisionError: 
            self.display.setText("0으로 나눌 수 없습니다")
            self.expression = ''
            self.last_was_equal = False
            self.adjust_display_font_size()
        except ValueError as ve: 
            self.display.setText("Error")
            print(f"Calculation Error (ValueError): {ve}") 
            self.expression = ''
            self.last_was_equal = False
            self.adjust_display_font_size()
        except Exception as e: 
            self.display.setText("Error")
            print(f"Unexpected Error: {type(e).__name__} - {e}") 
            self.expression = ''
            self.last_was_equal = False
            self.adjust_display_font_size()

    # 소수점 6자리 이하 반올림 출력
    def format_number(self, number):
        if not isinstance(number, (int, float)) or not (float('-inf') < number < float('inf')):
             return str(number) 
        s = str(number)
        if 'e' in s or 'E' in s: 
             return s

        # 소수점 6자리에서 반올림
        rounded_number = round(number, 6)
        formatted_str = f"{rounded_number:,}" 

        if '.' in formatted_str:
            parts = formatted_str.split('.') 
            integer_part = parts[0]
            decimal_part = parts[1]

            decimal_part = decimal_part.rstrip('0') 

            if decimal_part: 
                 formatted_str = integer_part + '.' + decimal_part
            else: 
                 formatted_str = integer_part

        if formatted_str == "-0":
            formatted_str = "0"
        if formatted_str in [".", "-"] and number == 0:
             formatted_str = "0"

        return formatted_str 

    def on_button_click(self):
        sender = self.sender() 
        text = sender.text() 

        if text == 'AC': self.reset()
        elif text == '±': self.negative_positive()
        elif text == '%': self.percent()
        elif text in '+-×÷': self.handle_operator(text)
        elif text == '.': self.handle_decimal()
        elif text == '=': self.equal()
        elif text.isdigit(): self.handle_digit(text)


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    calc = Calculator() 
    calc.show() 
    sys.exit(app.exec_()) 