"""UIパネル（サイドバーにサーバー状態表示）"""

import bpy
from bpy.types import Panel

from . import server


class BCLI_PT_ServerPanel(Panel):
    bl_label = "CLI Server"
    bl_idname = "BCLI_PT_server"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CLI Server"

    def draw(self, context):
        layout = self.layout
        running = server.is_running()

        if running:
            addr = server.get_address()
            host, port = addr if addr else ("?", "?")
            layout.label(text=f"Status: Running ({host}:{port})")
            layout.operator("bcli.stop_server", icon="PAUSE")
        else:
            layout.label(text="Status: Stopped")
            layout.operator("bcli.start_server", icon="PLAY")


panel_classes: list[type] = [
    BCLI_PT_ServerPanel,
]
