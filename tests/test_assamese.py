# -*- coding: utf-8 -*-
"""Tests for the Assamese language frontend."""

import pytest
from axomiscript import compile_source, run_source
from axomiscript.languages.assamese import parse
from axomiscript.core.ast_nodes import (
    Program,
    VarDecl,
    PrintStmt,
    IfStmt,
    LoopStmt,
    Number,
    StringLiteral,
    Identifier,
)
from axomiscript.generators import python_gen, cpp_gen
from axomiscript.languages.assamese.preprocessor import preprocess


class TestPreprocessor:
    def test_nagari_digits(self):
        assert preprocess("১০") == "10"
        assert preprocess("০১২৩৪৫৬৭৮৯") == "0123456789"

    def test_mixed(self):
        assert preprocess("চলক ক = ১০") == "চলক ক = 10"

    def test_ascii_unchanged(self):
        assert preprocess("abc 123") == "abc 123"


class TestParser:
    def test_var_decl(self):
        ast = parse("চলক ক = ১০\n")
        assert isinstance(ast, Program)
        assert len(ast.body) == 1
        node = ast.body[0]
        assert isinstance(node, VarDecl)
        assert node.name == "ক"
        assert isinstance(node.value, Number)
        assert node.value.value == 10

    def test_print_string(self):
        ast = parse('মুদ্ৰণ "নমস্কাৰ"\n')
        assert isinstance(ast.body[0], PrintStmt)
        assert isinstance(ast.body[0].value, StringLiteral)

    def test_if_stmt(self):
        src = 'যদি ক > ৫ {\n    মুদ্ৰণ "ডাঙৰ"\n}\n'
        ast = parse(src)
        assert isinstance(ast.body[0], IfStmt)

    def test_if_else(self):
        src = 'চলক ক = ১০\nযদি ক > ৫ {\n    মুদ্ৰণ "ডাঙৰ"\n}\nনহলে {\n    মুদ্ৰণ "সৰু"\n}\n'
        ast = parse(src)
        if_node = ast.body[1]
        assert isinstance(if_node, IfStmt)
        assert len(if_node.else_body) == 1

    def test_loop(self):
        src = "চক্ৰ ই = ১ লৈ ৫ {\n    মুদ্ৰণ ই\n}\n"
        ast = parse(src)
        assert isinstance(ast.body[0], LoopStmt)
        assert ast.body[0].var == "ই"

    def test_float(self):
        ast = parse("চলক x = 3.14\n")
        node = ast.body[0]
        assert isinstance(node.value, Number)
        assert node.value.value == 3.14


class TestPythonGenerator:
    def test_var_decl(self):
        ast = parse("চলক ক = ১০\n")
        code = python_gen.generate(ast)
        assert "ক = 10" in code

    def test_print(self):
        ast = parse('মুদ্ৰণ "নমস্কাৰ"\n')
        code = python_gen.generate(ast)
        assert 'print("নমস্কাৰ")' in code

    def test_loop(self):
        ast = parse("চক্ৰ ই = ১ লৈ ৫ {\n    মুদ্ৰণ ই\n}\n")
        code = python_gen.generate(ast)
        assert "for ই in range(1, 5 + 1):" in code


class TestCppGenerator:
    def test_var_decl(self):
        ast = parse("চলক ক = ১০\n")
        code = cpp_gen.generate(ast)
        assert "int ক = 10;" in code

    def test_string_u8(self):
        ast = parse('মুদ্ৰণ "নমস্কাৰ"\n')
        code = cpp_gen.generate(ast)
        assert 'u8"নমস্কাৰ"' in code

    def test_loop(self):
        ast = parse("চক্ৰ ই = ১ লৈ ৫ {\n    মুদ্ৰণ ই\n}\n")
        code = cpp_gen.generate(ast)
        assert "for (int ই = 1; ই <= 5; ++ই)" in code

    def test_includes(self):
        ast = parse("চলক ক = ১\n")
        code = cpp_gen.generate(ast)
        assert "#include <iostream>" in code


class TestCompiler:
    def test_compile_python(self):
        code = compile_source("চলক ক = ১০\nমুদ্ৰণ ক\n")
        assert "ক = 10" in code
        assert "print(" in code

    def test_compile_cpp(self):
        code = compile_source("চলক ক = ১০\nমুদ্ৰণ ক\n", target="cpp")
        assert "#include" in code
        assert "int ক = 10;" in code

    def test_compile_ast(self):
        code = compile_source("চলক ক = ১০\n", target="ast")
        assert "Program" in code

    def test_invalid_target(self):
        with pytest.raises(ValueError):
            compile_source("চলক ক = ১\n", target="javascript")

    def test_full_program(self):
        src = 'চলক ক = ১০\nযদি ক > ৫ {\n    মুদ্ৰণ "ডাঙৰ"\n}\nনহলে {\n    মুদ্ৰণ "সৰু"\n}\n'
        py = compile_source(src)
        assert "if" in py
        assert "else" in py


class TestExecutor:
    def test_run_print(self):
        result = run_source('মুদ্ৰণ "নমস্কাৰ"\n')
        assert result["exit_code"] == 0
        assert "নমস্কাৰ" in result["stdout"]

    def test_run_var(self):
        result = run_source("চলক ক = ৪২\nমুদ্ৰণ ক\n")
        assert "42" in result["stdout"]

    def test_run_loop(self):
        result = run_source("চক্ৰ ই = ১ লৈ ৩ {\n    মুদ্ৰণ ই\n}\n")
        assert "1" in result["stdout"]
        assert "3" in result["stdout"]
