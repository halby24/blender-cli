"""MainThreadDispatcher: サーバースレッドからBlenderメインスレッドへのタスクディスパッチャー"""

import logging
from threading import Event
from typing import Any, Callable

logger = logging.getLogger(__name__)


class MainThreadDispatcher:
    """1タスク1インスタンスの使い捨てディスパッチャー

    bpy.app.timers.register でメインスレッドにタスクを委譲し、
    threading.Event で同期的に結果を待機する。
    """

    def __init__(self, task: Callable[[], Any]):
        self.task = task
        self.done = Event()
        self.result: Any = None
        self.exception: Exception | None = None

    def dispatch(self, timeout: float | None = 10.0) -> Any:
        """タスクをメインスレッドで実行し、結果を同期的に待機する。

        Args:
            timeout: 待機タイムアウト秒数。Noneで無期限待機。

        Returns:
            タスクの実行結果

        Raises:
            TimeoutError: タイムアウトした場合
            Exception: メインスレッドでタスク実行中に発生した例外
        """
        import bpy

        bpy.app.timers.register(self._execute, first_interval=0.0)

        if not self.done.wait(timeout=timeout):
            raise TimeoutError("Main thread dispatch timed out")

        if self.exception is not None:
            raise self.exception

        return self.result

    def _execute(self) -> None:
        """メインスレッドでタスクを実行（bpy.app.timersから呼ばれる）"""
        try:
            self.result = self.task()
        except Exception as e:
            logger.error(f"Task execution failed: {e}", exc_info=True)
            self.exception = e
        finally:
            self.done.set()
