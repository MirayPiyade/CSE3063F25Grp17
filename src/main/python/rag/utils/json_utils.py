from typing import Any, Dict, List, Union, Optional
import re


class JsonUtils:
    @staticmethod
    def parse(json_str: str) -> Any:
        if json_str is None:
            raise ValueError("JSON input cannot be null")
        parser: JsonUtils._Parser = JsonUtils._Parser(json_str)
        value: Any = parser.parse_value()
        parser.skip_whitespace()
        if not parser.is_end():
            raise ValueError("Unexpected trailing data while parsing JSON")
        return value

    @staticmethod
    def expect_object(node: Any, message: str) -> Dict[str, Any]:
        if isinstance(node, dict):
            return node
        raise ValueError(message)

    @staticmethod
    def expect_array(node: Any, message: str) -> List[Any]:
        if isinstance(node, list):
            return node
        raise ValueError(message)

    @staticmethod
    def expect_string(node: Any, message: str) -> Optional[str]:
        if node is None:
            return None
        if isinstance(node, str):
            return node
        raise ValueError(message)

    @staticmethod
    def expect_number(node: Any, message: str) -> float:
        if isinstance(node, (int, float)):
            return float(node)
        raise ValueError(message)

    class _Parser:
        def __init__(self, input_str: str) -> None:
            self.input: str = input_str
            self.index: int = 0

        def parse_value(self) -> Any:
            self.skip_whitespace()
            if self.is_end():
                raise ValueError("Unexpected end of JSON input")
            c: str = self.input[self.index]
            if c == '{':
                return self.parse_object()
            elif c == '[':
                return self.parse_array()
            elif c == '"':
                return self.parse_string()
            elif c == 't':
                return self.parse_literal("true", True)
            elif c == 'f':
                return self.parse_literal("false", False)
            elif c == 'n':
                return self.parse_literal("null", None)
            elif c == '-' or c.isdigit():
                return self.parse_number()
            else:
                raise ValueError(f"Invalid JSON value starting at position {self.index}")

        def parse_object(self) -> Dict[str, Any]:
            self.expect('{')
            map_obj: Dict[str, Any] = {}
            self.skip_whitespace()
            if self.peek('}'):
                self.index += 1
                return map_obj
            while True:
                self.skip_whitespace()
                key: str = self.parse_string()
                self.skip_whitespace()
                self.expect(':')
                value: Any = self.parse_value()
                map_obj[key] = value
                self.skip_whitespace()
                if self.peek('}'):
                    self.index += 1
                    break
                self.expect(',')
            return map_obj

        def parse_array(self) -> List[Any]:
            self.expect('[')
            list_obj: List[Any] = []
            self.skip_whitespace()
            if self.peek(']'):
                self.index += 1
                return list_obj
            while True:
                value: Any = self.parse_value()
                list_obj.append(value)
                self.skip_whitespace()
                if self.peek(']'):
                    self.index += 1
                    break
                self.expect(',')
            return list_obj

        def parse_string(self) -> str:
            self.expect('"')
            sb: List[str] = []
            while not self.is_end():
                c: str = self.input[self.index]
                self.index += 1
                if c == '"':
                    return ''.join(sb)
                if c == '\\':
                    if self.is_end():
                        raise ValueError("Unterminated escape sequence in JSON string")
                    esc: str = self.input[self.index]
                    self.index += 1
                    if esc in ['"', '\\', '/']:
                        sb.append(esc)
                    elif esc == 'b':
                        sb.append('\b')
                    elif esc == 'f':
                        sb.append('\f')
                    elif esc == 'n':
                        sb.append('\n')
                    elif esc == 'r':
                        sb.append('\r')
                    elif esc == 't':
                        sb.append('\t')
                    elif esc == 'u':
                        if self.index + 4 > len(self.input):
                            raise ValueError("Invalid unicode escape in JSON string")
                        hex_str: str = self.input[self.index:self.index + 4]
                        sb.append(chr(int(hex_str, 16)))
                        self.index += 4
                    else:
                        raise ValueError(f"Unsupported escape: \\{esc}")
                else:
                    sb.append(c)
            raise ValueError("Unterminated JSON string")

        def parse_number(self) -> Union[int, float]:
            start: int = self.index
            if self.peek('-'):
                self.index += 1
            while not self.is_end() and self.input[self.index].isdigit():
                self.index += 1
            if not self.is_end() and self.input[self.index] == '.':
                self.index += 1
                while not self.is_end() and self.input[self.index].isdigit():
                    self.index += 1
            if not self.is_end() and self.input[self.index] in ['e', 'E']:
                self.index += 1
                if not self.is_end() and self.input[self.index] in ['+', '-']:
                    self.index += 1
                while not self.is_end() and self.input[self.index].isdigit():
                    self.index += 1
            value: float = float(self.input[start:self.index])
            if value == round(value):
                as_long: int = int(value)
                if -2147483648 <= as_long <= 2147483647:
                    return as_long
                return as_long
            return value

        def parse_literal(self, literal: str, value: Any) -> Any:
            if self.input[self.index:self.index + len(literal)] == literal:
                self.index += len(literal)
                return value
            raise ValueError(f"Invalid token at position {self.index}")

        def expect(self, expected: str) -> None:
            self.skip_whitespace()
            if self.is_end() or self.input[self.index] != expected:
                raise ValueError(f"Expected '{expected}' at position {self.index}")
            self.index += 1

        def peek(self, c: str) -> bool:
            self.skip_whitespace()
            return not self.is_end() and self.input[self.index] == c

        def skip_whitespace(self) -> None:
            while not self.is_end() and self.input[self.index].isspace():
                self.index += 1

        def is_end(self) -> bool:
            return self.index >= len(self.input)






