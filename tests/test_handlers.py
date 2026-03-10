"""RPCハンドラのユニットテスト"""

import time


class TestPing:
    def test_returns_version_and_timestamp(self, mock_bpy):
        from blender_cli.addon.handlers import ping

        before = time.time()
        result = ping()
        after = time.time()

        assert result["blender_version"] == "4.5.0"
        assert before <= result["timestamp"] <= after


class TestEval:
    def test_eval_simple_expression(self, mock_bpy):
        from blender_cli.addon.handlers import eval_expression

        result = eval_expression("1 + 2")
        assert result == 3

    def test_eval_list(self, mock_bpy):
        from blender_cli.addon.handlers import eval_expression

        result = eval_expression("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_eval_error(self, mock_bpy):
        import pytest
        from blender_cli.addon.handlers import eval_expression

        with pytest.raises(Exception):
            eval_expression("undefined_var")


class TestExec:
    def test_exec_simple_code(self, mock_bpy):
        from blender_cli.addon.handlers import exec_code

        result = exec_code("x = 1 + 1")
        assert result is None

    def test_exec_error(self, mock_bpy):
        import pytest
        from blender_cli.addon.handlers import exec_code

        with pytest.raises(Exception):
            exec_code("raise ValueError('test')")
