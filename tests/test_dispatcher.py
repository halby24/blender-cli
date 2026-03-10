"""MainThreadDispatcherテスト"""


class TestDispatcher:
    def test_dispatch_returns_result(self, mock_bpy):
        from blender_cli.addon.dispatcher import MainThreadDispatcher

        d = MainThreadDispatcher(lambda: 42)
        assert d.dispatch() == 42

    def test_dispatch_propagates_exception(self, mock_bpy):
        import pytest
        from blender_cli.addon.dispatcher import MainThreadDispatcher

        def failing_task():
            raise ValueError("test error")

        d = MainThreadDispatcher(failing_task)
        with pytest.raises(ValueError, match="test error"):
            d.dispatch()

    def test_execute_sets_done_event(self, mock_bpy):
        from blender_cli.addon.dispatcher import MainThreadDispatcher

        d = MainThreadDispatcher(lambda: "hello")
        assert not d.done.is_set()
        d._execute()
        assert d.done.is_set()
        assert d.result == "hello"
