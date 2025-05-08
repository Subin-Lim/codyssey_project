import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QFont


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

        self.initial_font_size = 30
        self.min_font_size = 10
        self.base_display_style = 'background-color: black; color: white; padding: 10px;'

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(self.display)

        grid_layout = QGridLayout()
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+']
        ]

        for row, texts in enumerate(buttons):
            for col, text in enumerate(texts):
                button = QPushButton(text)
                button.setFixedSize(60, 60)
                style = 'font-size: 20px; color: white; border: none;'
                if text in ['÷', '×', '-', '+']:
                    style += ' background-color: #f57c00;'
                elif text in ['AC', '±', '%']:
                    style += ' color: black; background-color: #a5a5a5;'
                else:
                    style += ' background-color: #333;'
                button.setStyleSheet(style)
                button.clicked.connect(self.on_button_click)
                grid_layout.addWidget(button, row + 1, col)

        zero_button = QPushButton('0')
        zero_button.setFixedSize(130, 60)
        zero_button.setStyleSheet('font-size: 20px; color: white; background-color: #333; border: none; text-align: left; padding-left: 15px;')
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
        self.adjust_display_font_size()

    def adjust_display_font_size(self):
        text = self.display.text()
        if not text:
            return
        available_width = self.display.width() - 20
        test_font = QFont(self.display.font())
        for size in range(self.initial_font_size, self.min_font_size - 1, -1):
            test_font.setPixelSize(size)
            if QFontMetrics(test_font).horizontalAdvance(text) <= available_width:
                self.display.setStyleSheet(f'font-size: {size}px; {self.base_display_style}')
                return
        self.display.setStyleSheet(f'font-size: {self.min_font_size}px; {self.base_display_style}')

    def format_number(self, number):
        try:
            rounded = round(number, 6)
            if abs(rounded) > 1e15:
                return "N/A"
            s = f"{rounded:,.6f}".rstrip('0').rstrip('.')
            return s if s != '-0' else '0'
        except:
            return "Error"

    def reset(self):
        self.expression = ''
        self.last_was_equal = False
        self.update_display_text()

    def negative_positive(self):
        match = re.search(r'([+\-×÷])?(-?\d+\.?\d*|\.\d+)$', self.expression)
        if match:
            num = match.group(2)
            start = match.start(2)
            try:
                toggled = str(-float(num))
                self.expression = self.expression[:start] + toggled
                self.update_display_text()
            except:
                self.display.setText("Error")

    def percent(self):
        match = re.search(r'(-?\d+\.?\d*|\.\d+)$', self.expression)
        if match:
            num = match.group(0)
            start = match.start(0)
            try:
                percented = str(float(num) / 100)
                self.expression = self.expression[:start] + percented
                self.update_display_text()
            except:
                self.display.setText("Error")

    def handle_digit(self, digit):
        if self.last_was_equal:
            self.expression = digit
        else:
            if self.expression.endswith('0') and not '.' in self.expression.split()[-1]:
                self.expression = self.expression[:-1] + digit
            else:
                self.expression += digit
        self.last_was_equal = False
        self.update_display_text()

    def handle_decimal(self):
        if self.last_was_equal:
            self.expression = '0.'
        else:
            last_op = max([self.expression.rfind(op) for op in '+-×÷'] + [-1])
            segment = self.expression[last_op + 1:]
            if '.' not in segment:
                self.expression += '.' if segment else '0.'
        self.last_was_equal = False
        self.update_display_text()

    def handle_operator(self, op):
        if not self.expression and op != '-':
            return
        if self.last_was_equal:
            self.last_was_equal = False
        if self.expression and self.expression[-1] in '+-×÷':
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self.update_display_text()

    def tokenize_and_process(self, expr):
        raw = re.findall(r'\d*\.?\d+|\.\d+|[+\-×÷]', expr)
        processed = []
        i = 0
        while i < len(raw):
            if raw[i] == '-' and (i == 0 or raw[i-1] in '+-×÷'):
                processed.append(float('-' + raw[i+1]))
                i += 2
            elif raw[i] in '+×÷':
                processed.append(raw[i])
                i += 1
            else:
                processed.append(float(raw[i]))
                i += 1
        return processed

    def evaluate_operations(self, tokens, ops):
        i = 0
        while i < len(tokens):
            if tokens[i] in ops:
                a, b = tokens[i-1], tokens[i+1]
                op = tokens[i]
                if op == '×': res = a * b
                elif op == '÷': res = self.divide(a, b)
                elif op == '+': res = a + b
                elif op == '-': res = a - b
                tokens[i-1:i+2] = [res]
                i -= 1
            else:
                i += 1
        return tokens

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    def equal(self):
        if self.last_was_equal:
            return
        expr = self.expression.rstrip('+-×÷')
        if not expr:
            self.reset()
            return
        try:
            tokens = self.tokenize_and_process(expr)
            tokens = self.evaluate_operations(tokens, ['×', '÷'])
            tokens = self.evaluate_operations(tokens, ['+', '-'])
            if len(tokens) == 1:
                result = tokens[0]
                self.display.setText(self.format_number(result))
                self.expression = str(result)
                self.last_was_equal = True
            else:
                raise ValueError
        except ZeroDivisionError:
            self.display.setText("0으로 나눌 수 없습니다")
        except:
            self.display.setText("Error")
        finally:
            self.adjust_display_font_size()

    def update_display_text(self):
        self.display.setText(self.expression if self.expression else '0')
        self.adjust_display_font_size()

    def on_button_click(self):
        text = self.sender().text()
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
