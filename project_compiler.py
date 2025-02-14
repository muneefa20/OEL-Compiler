import ipywidgets as widgets
from IPython.display import display
import re

# Define token types
TOKEN_TYPES = {
    'NUMBER': r'\d+',
    'PLUS': r'\+',
    'MINUS': r'-',
    'TIMES': r'\*',
    'DIVIDE': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'ASSIGN': r'=',
    'ID': r'[a-zA-Z_]\w*',  # Variable name (identifier)
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text.strip()  # Remove leading and trailing whitespace
        self.pos = 0

    def error(self):
        raise Exception('Invalid character: {}'.format(self.text[self.pos]))

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token('EOF', None)

        print("Current character:", self.text[self.pos])

        for token_type, pattern in TOKEN_TYPES.items():
            regex = re.compile('^' + pattern)
            match = regex.match(self.text[self.pos:])
            if match:
                value = match.group(0)
                token = Token(token_type, value)
                self.pos += len(value)
                return token

        self.error()

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            self.expr()
            self.eat('RPAREN')
        elif token.type == 'ID':
            self.eat('ID')
        else:
            self.error()

    def term(self):
        self.factor()
        while self.current_token.type in ('TIMES', 'DIVIDE'):
            token = self.current_token
            if token.type == 'TIMES':
                self.eat('TIMES')
            elif token.type == 'DIVIDE':
                self.eat('DIVIDE')
            self.factor()

    def expr(self):
        self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
            elif token.type == 'MINUS':
                self.eat('MINUS')
            self.term()

class CodeEditorApp:
    def __init__(self):
        self.text_box = widgets.Textarea(layout=widgets.Layout(width='80%', height='200px'))
        self.check_syntax_button = widgets.Button(description="Check Syntax")
        self.execute_button = widgets.Button(description="Execute")
        self.error_logger = widgets.Output(layout=widgets.Layout(width='80%', height='100px'))

        self.check_syntax_button.on_click(self.check_syntax)
        self.execute_button.on_click(self.execute_code)

        self.main_box = widgets.VBox([
            self.text_box,
            widgets.HBox([self.check_syntax_button, self.execute_button]),
            self.error_logger
        ])

        display(self.main_box)

    def check_syntax(self, b):
        # Get the code from the text box
        code = self.text_box.value

        # Perform lexical analysis (tokenization)
        try:
            lexer = Lexer(code)
            while lexer.get_next_token().type != 'EOF':
                pass
            self.error_logger.clear_output()
            with self.error_logger:
                print("Syntax check completed. No errors found.")
        except Exception as e:
            self.error_logger.clear_output()
            with self.error_logger:
                print(f"Syntax error: {e}")

    def execute_code(self, b):
        # Get the code from the text box
        code = self.text_box.value

        # Create parser and parse the code
        parser = Parser(code)
        try:
            parser.expr()
            self.error_logger.clear_output()
            with self.error_logger:
                print("Code execution completed.")
        except Exception as e:
            self.error_logger.clear_output()
            with self.error_logger:
                print(f"Execution error: {e}")

app = CodeEditorApp()
