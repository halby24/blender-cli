"""CLIクライアントテスト"""

import pytest


class TestClient:
    def test_ping(self, rpc_client):
        result = rpc_client.call("ping")
        assert "blender_version" in result
        assert "timestamp" in result

    def test_eval(self, rpc_client):
        result = rpc_client.call("eval", expression="1 + 1")
        assert result == 2

    def test_exec(self, rpc_client):
        result = rpc_client.call("exec", code="x = 1")
        assert result is None

    def test_connection_error(self):
        from blender_cli.cli.client import JsonRpcClient

        client = JsonRpcClient(port=1)  # 接続不可能なポート
        with pytest.raises(ConnectionError):
            client.call("ping")

    def test_rpc_error(self, rpc_client):
        with pytest.raises(RuntimeError, match="Method not found"):
            rpc_client.call("nonexistent")
