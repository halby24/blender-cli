"""テスト共通fixture"""

import json
import socket
import threading
import time
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture()
def mock_bpy():
    """bpyモジュールのモック"""
    bpy_mock = MagicMock()
    bpy_mock.app.version_string = "4.5.0"
    bpy_mock.app.timers = MagicMock()

    # timers.register はコールバックを即座に呼ぶ
    def fake_register(func, first_interval=0.0):
        func()

    bpy_mock.app.timers.register = fake_register

    modules = {
        "bpy": bpy_mock,
        "bpy.app": bpy_mock.app,
        "bpy.app.timers": bpy_mock.app.timers,
        "bpy.types": bpy_mock.types,
        "bpy.props": bpy_mock.props,
        "bpy.utils": bpy_mock.utils,
    }

    with patch.dict("sys.modules", modules):
        yield bpy_mock


@pytest.fixture()
def rpc_server(mock_bpy):
    """テスト用JSON-RPCサーバーを起動・停止"""
    from blender_cli.addon.server import start, stop, get_address

    start("127.0.0.1", 0)  # ポート0で空きポートを自動割り当て
    addr = get_address()
    yield addr
    stop()


@pytest.fixture()
def rpc_client(rpc_server):
    """テスト用クライアント"""
    from blender_cli.cli.client import JsonRpcClient

    host, port = rpc_server
    return JsonRpcClient(host=host, port=port)


def send_raw_rpc(host: str, port: int, request: dict | str) -> dict:
    """テスト用: 生のJSON-RPCリクエストを送信してレスポンスを返す"""
    with socket.create_connection((host, port), timeout=5.0) as sock:
        if isinstance(request, dict):
            data = json.dumps(request) + "\n"
        else:
            data = request + "\n"
        sock.sendall(data.encode("utf-8"))
        fp = sock.makefile("r", encoding="utf-8")
        line = fp.readline()
        return json.loads(line) if line else {}
