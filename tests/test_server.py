"""サーバーのJSON-RPCプロトコルテスト"""

from conftest import send_raw_rpc


class TestJsonRpcProtocol:
    def test_valid_request(self, rpc_server):
        host, port = rpc_server
        resp = send_raw_rpc(host, port, {
            "jsonrpc": "2.0", "method": "ping", "params": {}, "id": 1
        })
        assert resp["jsonrpc"] == "2.0"
        assert resp["id"] == 1
        assert "result" in resp

    def test_invalid_json(self, rpc_server):
        host, port = rpc_server
        resp = send_raw_rpc(host, port, "not valid json")
        assert resp["error"]["code"] == -32700

    def test_method_not_found(self, rpc_server):
        host, port = rpc_server
        resp = send_raw_rpc(host, port, {
            "jsonrpc": "2.0", "method": "nonexistent", "params": {}, "id": 2
        })
        assert resp["error"]["code"] == -32601

    def test_invalid_request_missing_jsonrpc(self, rpc_server):
        host, port = rpc_server
        resp = send_raw_rpc(host, port, {
            "method": "ping", "id": 3
        })
        assert resp["error"]["code"] == -32600

    def test_server_start_stop(self, mock_bpy):
        from blender_cli.addon import server

        assert not server.is_running()
        assert server.start("127.0.0.1", 0)
        assert server.is_running()
        assert server.get_address() is not None
        assert server.stop()
        assert not server.is_running()
