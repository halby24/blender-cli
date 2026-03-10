"""サーバー起動/停止オペレータ"""

from bpy.types import Context, Operator

from . import server


class BCLI_OT_StartServer(Operator):
    """JSON-RPCサーバーを起動する"""

    bl_idname = "bcli.start_server"
    bl_label = "Start CLI Server"

    def execute(self, context: Context):
        if server.is_running():
            self.report({"INFO"}, "サーバーは既に起動しています")
        elif server.start():
            self.report({"INFO"}, "サーバーを起動しました")
        else:
            self.report({"ERROR"}, "サーバーの起動に失敗しました")
            return {"CANCELLED"}
        return {"FINISHED"}


class BCLI_OT_StopServer(Operator):
    """JSON-RPCサーバーを停止する"""

    bl_idname = "bcli.stop_server"
    bl_label = "Stop CLI Server"

    def execute(self, context: Context):
        if not server.is_running():
            self.report({"INFO"}, "サーバーは起動していません")
        elif server.stop():
            self.report({"INFO"}, "サーバーを停止しました")
        else:
            self.report({"ERROR"}, "サーバーの停止に失敗しました")
            return {"CANCELLED"}
        return {"FINISHED"}


operator_classes: list[type] = [
    BCLI_OT_StartServer,
    BCLI_OT_StopServer,
]
