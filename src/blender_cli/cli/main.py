"""CLIエントリポイント"""

import argparse
import json
import sys

from .client import JsonRpcClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="blender-cli",
        description="Control a running Blender instance via JSON-RPC",
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=8799, help="Server port (default: 8799)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ping
    subparsers.add_parser("ping", help="Check connection to Blender")

    # eval
    eval_parser = subparsers.add_parser("eval", help="Evaluate a Python expression")
    eval_parser.add_argument("expression", help="Python expression to evaluate")

    # exec
    exec_parser = subparsers.add_parser("exec", help="Execute Python code")
    exec_parser.add_argument("code", help="Python code to execute")

    args = parser.parse_args(argv)
    client = JsonRpcClient(host=args.host, port=args.port)

    try:
        if args.command == "ping":
            result = client.call("ping")
            print(json.dumps(result, indent=2))

        elif args.command == "eval":
            result = client.call("eval", expression=args.expression)
            print(json.dumps(result, indent=2) if not isinstance(result, str) else result)

        elif args.command == "exec":
            client.call("exec", code=args.code)
            print("OK")

    except ConnectionError as e:
        print(f"Connection error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
