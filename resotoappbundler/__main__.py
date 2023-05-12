import sys
import json
from pathlib import Path
from resotolib.logger import log, setup_logger, add_args as logging_add_args
from resotolib.args import ArgumentParser
from .app import app_manifest, app_dry_run, add_args as app_add_args


def main() -> None:
    setup_logger("resotoappbundler")

    arg_parser = ArgumentParser(description="Resoto Infrastructure Apps Bundler")
    app_add_args(arg_parser)
    logging_add_args(arg_parser)
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
        sys.exit(0)

    manifest = app_manifest(app_path)
    if arg_parser.args.dry_run:
        app_dry_run(manifest)
    else:
        print(json.dumps(manifest))

    sys.exit(0)


if __name__ == "__main__":
    main()
