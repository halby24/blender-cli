"""JSON-RPC 2.0 over TCP サーバー"""

import json
import logging
import socketserver
import threading
from typing import Any, Optional

from .handlers import METHOD_TABLE

logger = logging.getLogger(__name__)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8799

_server: Optional[socketserver.TCPServer] = None
_server_thread: Optional[threading.Thread] = None


class JsonRpcHandler(socketserver.StreamRequestHandler):
    """JSON-RPC 2.0リクエストを処理するハンドラ"""

    def handle(self):
        try:
            raw = self.rfile.readline()
            if not raw:
                return

            request = json.loads(raw.decode("utf-8"))
            response = _process_request(request)

            if response is not None:
                data = json.dumps(response, ensure_ascii=False) + "\n"
                self.wfile.write(data.encode("utf-8"))
                self.wfile.flush()

        except json.JSONDecodeError:
            error_resp = _error_response(None, -32700, "Parse error")
            data = json.dumps(error_resp) + "\n"
            self.wfile.write(data.encode("utf-8"))
            self.wfile.flush()
        except Exception as e:
            logger.error(f"Handler error: {e}", exc_info=True)


def _process_request(request: dict) -> Optional[dict]:
    """JSON-RPCリクエストを処理してレスポンスを返す"""
    if not isinstance(request, dict):
        return _error_response(None, -32600, "Invalid Request")

    jsonrpc = request.get("jsonrpc")
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")

    if jsonrpc != "2.0" or not isinstance(method, str):
        return _error_response(req_id, -32600, "Invalid Request")

    handler = METHOD_TABLE.get(method)
    if handler is None:
        return _error_response(req_id, -32601, f"Method not found: {method}")

    try:
        if isinstance(params, dict):
            result = handler(**params)
        elif isinstance(params, list):
            result = handler(*params)
        else:
            result = handler()

        # Notification (id なし) の場合はレスポンスを返さない
        if req_id is None:
            return None

        return {"jsonrpc": "2.0", "result": result, "id": req_id}

    except TypeError as e:
        return _error_response(req_id, -32602, f"Invalid params: {e}")
    except Exception as e:
        return _error_response(req_id, -32000, str(e))


def _error_response(req_id: Any, code: int, message: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "error": {"code": code, "message": message},
        "id": req_id,
    }


def start(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> bool:
    """サーバーを起動する"""
    global _server, _server_thread

    if is_running():
        logger.warning("サーバーは既に起動しています")
        return False

    try:
        socketserver.TCPServer.allow_reuse_address = True
        _server = socketserver.TCPServer((host, port), JsonRpcHandler)

        _server_thread = threading.Thread(
            target=_server.serve_forever,
            daemon=True,
        )
        _server_thread.start()

        logger.info(f"JSON-RPCサーバー起動: {host}:{port}")
        return True

    except Exception as e:
        logger.error(f"サーバー起動失敗: {e}")
        _server = None
        _server_thread = None
        return False


def stop() -> bool:
    """サーバーを停止する"""
    global _server, _server_thread

    if not is_running():
        logger.warning("起動しているサーバーがありません")
        return False

    try:
        _server.shutdown()
        _server_thread.join(timeout=5.0)
        _server.server_close()
        logger.info("JSON-RPCサーバー停止")
        return True
    except Exception as e:
        logger.error(f"サーバー停止失敗: {e}")
        return False
    finally:
        _server = None
        _server_thread = None


def is_running() -> bool:
    """サーバーが起動中か確認する"""
    return _server_thread is not None and _server_thread.is_alive()


def get_address() -> tuple[str, int] | None:
    """起動中サーバーのアドレスを返す"""
    if _server is not None:
        return _server.server_address
    return None
