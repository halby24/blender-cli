"""RPCメソッド実装"""

import time
from typing import Any

from .dispatcher import MainThreadDispatcher


def ping() -> dict[str, Any]:
    """接続確認。タイムスタンプとBlenderバージョンを返す。"""
    import bpy

    return {
        "timestamp": time.time(),
        "blender_version": bpy.app.version_string,
    }


def eval_expression(expression: str) -> Any:
    """Python式をBlenderメインスレッドで評価して結果を返す。"""

    def task():
        import bpy  # noqa: F401

        return eval(expression)

    dispatcher = MainThreadDispatcher(task)
    result = dispatcher.dispatch()

    # JSON-RPCで返せるようにシリアライズ
    return _make_serializable(result)


def exec_code(code: str) -> None:
    """PythonコードをBlenderメインスレッドで実行する。"""

    def task():
        import bpy  # noqa: F401

        exec(code)

    dispatcher = MainThreadDispatcher(task)
    dispatcher.dispatch()
    return None


def _make_serializable(obj: Any) -> Any:
    """JSONシリアライズ可能な形に変換する。"""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {str(k): _make_serializable(v) for k, v in obj.items()}
    return str(obj)


# メソッド名 → ハンドラ関数のマッピング
METHOD_TABLE: dict[str, Any] = {
    "ping": ping,
    "eval": eval_expression,
    "exec": exec_code,
}
