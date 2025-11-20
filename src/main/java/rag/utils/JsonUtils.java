package rag.utils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Minimal JSON parser to avoid third-party dependencies.
 * Supports the subset we need for configuration and index files.
 */
public final class JsonUtils {

    private JsonUtils() {}

    public static Object parse(String json) {
        if (json == null) {
            throw new IllegalArgumentException("JSON input cannot be null");
        }
        Parser parser = new Parser(json);
        Object value = parser.parseValue();
        parser.skipWhitespace();
        if (!parser.isEnd()) {
            throw new IllegalArgumentException("Unexpected trailing data while parsing JSON");
        }
        return value;
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> expectObject(Object node, String message) {
        if (node instanceof Map<?, ?> map) {
            return (Map<String, Object>) map;
        }
        throw new IllegalArgumentException(message);
    }

    @SuppressWarnings("unchecked")
    public static List<Object> expectArray(Object node, String message) {
        if (node instanceof List<?> list) {
            return (List<Object>) list;
        }
        throw new IllegalArgumentException(message);
    }

    public static String expectString(Object node, String message) {
        if (node == null) return null;
        if (node instanceof String s) {
            return s;
        }
        throw new IllegalArgumentException(message);
    }

    public static double expectNumber(Object node, String message) {
        if (node instanceof Number number) {
            return number.doubleValue();
        }
        throw new IllegalArgumentException(message);
    }

    private static final class Parser {
        private final String input;
        private int index;

        Parser(String input) {
            this.input = input;
            this.index = 0;
        }

        Object parseValue() {
            skipWhitespace();
            if (isEnd()) {
                throw new IllegalArgumentException("Unexpected end of JSON input");
            }
            char c = input.charAt(index);
            return switch (c) {
                case '{' -> parseObject();
                case '[' -> parseArray();
                case '"' -> parseString();
                case 't' -> parseLiteral("true", Boolean.TRUE);
                case 'f' -> parseLiteral("false", Boolean.FALSE);
                case 'n' -> parseLiteral("null", null);
                default -> {
                    if (c == '-' || Character.isDigit(c)) {
                        yield parseNumber();
                    }
                    throw new IllegalArgumentException("Invalid JSON value starting at position " + index);
                }
            };
        }

        private Map<String, Object> parseObject() {
            expect('{');
            Map<String, Object> map = new HashMap<>();
            skipWhitespace();
            if (peek('}')) {
                index++;
                return map;
            }
            while (true) {
                skipWhitespace();
                String key = parseString();
                skipWhitespace();
                expect(':');
                Object value = parseValue();
                map.put(key, value);
                skipWhitespace();
                if (peek('}')) {
                    index++;
                    break;
                }
                expect(',');
            }
            return map;
        }

        private List<Object> parseArray() {
            expect('[');
            List<Object> list = new ArrayList<>();
            skipWhitespace();
            if (peek(']')) {
                index++;
                return list;
            }
            while (true) {
                Object value = parseValue();
                list.add(value);
                skipWhitespace();
                if (peek(']')) {
                    index++;
                    break;
                }
                expect(',');
            }
            return list;
        }

        private String parseString() {
            expect('"');
            StringBuilder sb = new StringBuilder();
            while (!isEnd()) {
                char c = input.charAt(index++);
                if (c == '"') {
                    return sb.toString();
                }
                if (c == '\\') {
                    if (isEnd()) {
                        throw new IllegalArgumentException("Unterminated escape sequence in JSON string");
                    }
                    char esc = input.charAt(index++);
                    switch (esc) {
                        case '"', '\\', '/' -> sb.append(esc);
                        case 'b' -> sb.append('\b');
                        case 'f' -> sb.append('\f');
                        case 'n' -> sb.append('\n');
                        case 'r' -> sb.append('\r');
                        case 't' -> sb.append('\t');
                        case 'u' -> {
                            if (index + 4 > input.length()) {
                                throw new IllegalArgumentException("Invalid unicode escape in JSON string");
                            }
                            String hex = input.substring(index, index + 4);
                            sb.append((char) Integer.parseInt(hex, 16));
                            index += 4;
                        }
                        default -> throw new IllegalArgumentException("Unsupported escape: \\" + esc);
                    }
                } else {
                    sb.append(c);
                }
            }
            throw new IllegalArgumentException("Unterminated JSON string");
        }

        private Number parseNumber() {
            int start = index;
            if (peek('-')) index++;
            while (!isEnd() && Character.isDigit(input.charAt(index))) index++;
            if (!isEnd() && input.charAt(index) == '.') {
                index++;
                while (!isEnd() && Character.isDigit(input.charAt(index))) index++;
            }
            if (!isEnd() && (input.charAt(index) == 'e' || input.charAt(index) == 'E')) {
                index++;
                if (!isEnd() && (input.charAt(index) == '+' || input.charAt(index) == '-')) index++;
                while (!isEnd() && Character.isDigit(input.charAt(index))) index++;
            }
            double value = Double.parseDouble(input.substring(start, index));
            if (value == Math.rint(value)) {
                long asLong = (long) value;
                if (asLong >= Integer.MIN_VALUE && asLong <= Integer.MAX_VALUE) {
                    return (int) asLong;
                }
                return asLong;
            }
            return value;
        }

        private Object parseLiteral(String literal, Object value) {
            if (input.startsWith(literal, index)) {
                index += literal.length();
                return value;
            }
            throw new IllegalArgumentException("Invalid token at position " + index);
        }

        private void expect(char expected) {
            skipWhitespace();
            if (isEnd() || input.charAt(index) != expected) {
                throw new IllegalArgumentException("Expected '" + expected + "' at position " + index);
            }
            index++;
        }

        private boolean peek(char c) {
            skipWhitespace();
            return !isEnd() && input.charAt(index) == c;
        }

        private void skipWhitespace() {
            while (!isEnd() && Character.isWhitespace(input.charAt(index))) {
                index++;
            }
        }

        private boolean isEnd() {
            return index >= input.length();
        }
    }
}
