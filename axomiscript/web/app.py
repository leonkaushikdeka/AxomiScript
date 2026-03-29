# -*- coding: utf-8 -*-
"""Flask web IDE for AxomiScript."""
from __future__ import annotations
import os
from flask import Flask, render_template, request, jsonify
from ..compiler import compile_source
from ..executor import run_source
from ..languages import available


def create_app() -> Flask:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    static_dir   = os.path.join(os.path.dirname(__file__), "static")
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    @app.route("/")
    def index():
        return render_template("index.html", languages=available())

    @app.route("/api/compile", methods=["POST"])
    def api_compile():
        data     = request.get_json()
        source   = data.get("source", "")
        language = data.get("language", "assamese")
        target   = data.get("target", "python")

        try:
            output = compile_source(source, language=language, target=target)
            return jsonify({"ok": True, "output": output})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

    @app.route("/api/run", methods=["POST"])
    def api_run():
        data     = request.get_json()
        source   = data.get("source", "")
        language = data.get("language", "assamese")

        try:
            result = run_source(source, language=language, timeout=10)
            return jsonify({
                "ok":       result["exit_code"] == 0,
                "stdout":   result["stdout"],
                "stderr":   result["stderr"],
                "python":   result["python_code"],
                "exit_code": result["exit_code"],
            })
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

    return app
