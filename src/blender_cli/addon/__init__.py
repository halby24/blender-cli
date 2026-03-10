from typing import Any

import bpy

from .operators import operator_classes
from .panels import panel_classes

bl_info: dict[str, Any] = {
    "name": "Blender CLI Server",
    "author": "HALBY",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > CLI Server",
    "description": "JSON-RPC server for CLI control of Blender",
    "category": "Development",
}

_classes = operator_classes + panel_classes


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    print("Blender CLI Server: アドオンが有効化されました")


def unregister():
    from . import server

    if server.is_running():
        server.stop()

    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
    print("Blender CLI Server: アドオンが無効化されました")
