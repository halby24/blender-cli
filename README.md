# blender-cli

起動中のBlenderインスタンスをCLIから操作するためのツール。
Blenderアドオン（JSON-RPC 2.0 TCPサーバー）とCLIクライアントで構成。

## セットアップ

### 依存インストール

```bash
uv sync
```

### Blenderアドオン

`src/blender_cli/addon/` をBlender 5.0のExtensionsディレクトリにシンボリックリンク:

```bash
# Windows (管理者権限 or 開発者モード)
python -c "import os; os.symlink(r'<repo>/src/blender_cli/addon', r'<extensions>/user_default/blender_cli', target_is_directory=True)"
```

Blenderの `編集 > Preferences > Add-ons` から **Blender CLI Server** を有効化。
3Dビューポートのサイドバー「CLI Server」タブからサーバーを起動。

## 使い方

```bash
# 接続確認
blender-cli ping

# Python式を評価
blender-cli eval "bpy.data.objects.keys()"

# Pythonコードを実行
blender-cli exec "bpy.ops.mesh.primitive_cube_add()"
```

### オプション

```
--host HOST  サーバーホスト (default: 127.0.0.1)
--port PORT  サーバーポート (default: 8799)
```

## テスト

```bash
uv run pytest
```

## License

[MIT](LICENSE)
