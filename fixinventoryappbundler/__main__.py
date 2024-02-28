import sys
import json
from pathlib import Path
from fixlib.logger import log, setup_logger, add_args as logging_add_args
from fixlib.args import ArgumentParser
from .runner import app_dry_run, add_args as runner_add_args
from .bundler import app_manifest, add_args as bundler_add_args


def main() -> None:
    print("Call fixinventoryappbundler or fixinventoryapprunner")
    sys.exit(1)


def add_args(arg_parser: ArgumentParser) -> None:
    arg_parser.add_argument(
        "--path",
        "-p",
        help="Path to app bundle(s)",
        dest="app_path",
        required=True,
        type=str,
    )


def bundle() -> None:
    setup_logger("fixinventoryappbundler")
    arg_parser = ArgumentParser(description="Fix Inventory Infrastructure Apps Bundler")
    logging_add_args(arg_parser)
    add_args(arg_parser)
    bundler_add_args(arg_parser)
    arg_parser.parse_args()

    app_path = Path(arg_parser.args.app_path)
    if not app_path.is_dir():
        log.error(f"Path {app_path} is not a directory")
        sys.exit(1)

    if arg_parser.args.discover:
        manifests = []
        for path in app_path.iterdir():
            if path.is_dir():
                try:
                    manifest = app_manifest(path)
                except Exception as e:
                    log.error(f"Failed to process {path}: {e}")
                    continue
                manifests.append(manifest)
        print(json.dumps(manifests))
    else:
        manifest = app_manifest(app_path)
        print(json.dumps(manifest))
    sys.exit(0)


def run() -> None:
    setup_logger("fixinventoryapprunner")
    arg_parser = ArgumentParser(description="Fix Inventory Infrastructure Apps Runner")
    logging_add_args(arg_parser)
    add_args(arg_parser)
    runner_add_args(arg_parser)
    args, argv = arg_parser.parse_known_args()

    app_path = Path(args.app_path)
    if not app_path.is_dir():
        log.error(f"Path {app_path} is not a directory")
        sys.exit(1)

    app_dry_run(app_manifest(app_path), args.config_path, argv)


if __name__ == "__main__":
    main()
