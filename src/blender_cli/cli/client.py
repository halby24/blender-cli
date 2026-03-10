"""JSON-RPCクライアント"""

import json
import socket
from typing import Any


class JsonRpcClient:
    """JSON-RPC 2.0 over TCP クライアント"""

    def __init__(self, host: str = "127.0.0.1", port: int = 8799):
        self.host = host
        self.port = port
        self._next_id = 1

    def call(self, method: str, **params: Any) -> Any:
        """JSON-RPCメソッドを呼び出し、結果を返す。

        Args:
            method: メソッド名
            **params: メソッドパラメータ

        Returns:
            レスポンスの result フィールド

        Raises:
            ConnectionError: 接続できない場合
            RuntimeError: JSON-RPCエラーレスポンスの場合
        """
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params if params else {},
            "id": self._next_id,
        }
        self._next_id += 1

        try:
            with socket.create_connection(
                (self.host, self.port), timeout=10.0
            ) as sock:
                data = json.dumps(request, ensure_ascii=False) + "\n"
                sock.sendall(data.encode("utf-8"))

                # レスポンスを読む
                fp = sock.makefile("r", encoding="utf-8")
                line = fp.readline()
                if not line:
                    raise ConnectionError("Empty response from server")

                response = json.loads(line)

        except (ConnectionRefusedError, OSError) as e:
            raise ConnectionError(
                f"Cannot connect to Blender at {self.host}:{self.port}: {e}"
            ) from e

        if "error" in response:
            err = response["error"]
            raise RuntimeError(f"RPC error {err['code']}: {err['message']}")

        return response.get("result")
