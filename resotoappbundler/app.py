import yaml
import base64
import hashlib
from pathlib import Path
from jinja2 import Environment
from resotolib.logger import log
from resotolib.args import ArgumentParser
from resotolib.durations import parse_optional_duration
from resotolib.core.search import CoreGraph
from resotolib.core.ca import TLSData
from resotolib.core import add_args as core_add_args, resotocore
from resotolib.jwt import add_args as jwt_add_args
from typing import Dict, List, Union, Optional


def add_args(arg_parser: ArgumentParser) -> None:
    group = arg_parser.add_mutually_exclusive_group()
    TLSData.add_args(arg_parser)
    core_add_args(arg_parser)
    jwt_add_args(arg_parser)
    arg_parser.add_argument(
        "--path",
        "-p",
        help="Path to app bundle(s)",
        dest="app_path",
        required=True,
        type=str,
    )

    group.add_argument(
        "--discover",
        help="Find all apps in the path",
        dest="discover",
        required=False,
        action="store_true",
    )

    group.add_argument(
        "--dry-run",
        help="Dry run the app",
        dest="dry_run",
        required=False,
        action="store_true",
    )

    arg_parser.add_argument(
        "--config",
        help="Path to app config",
        dest="config_path",
        required=False,
        default=None,
        type=str,
    )
    arg_parser.add_argument(
        "--subscriber-id",
        help="Unique subscriber ID (default: resotoappbundler)",
        default="resotoappbundler",
        dest="subscriber_id",
        type=str,
    )


def app_manifest(app_path: Path) -> Dict[str, Union[str, List, Dict]]:
    app_manifest = app_path / "app.yaml"
    app_readme = app_path / "README.md"
    app_source = app_path / "app.jinja2"
    app_icon = app_path / "app.svg"
    for file in [app_manifest, app_readme, app_source, app_icon]:
        if not file.exists():
            raise RuntimeError(f"Path {file} does not exist")

    source = app_source.read_text()
    manifest = yaml.load(app_manifest.read_text(), Loader=yaml.FullLoader)

    for key in ["name", "description", "version", "language", "license", "authors", "url", "categories", "default_config", "config_schema", "args_schema"]:
        if key not in manifest:
            raise ValueError(f"Key {key} is missing from {app_manifest}")

    readme = app_readme.read_text()
    icon = "data:image/svg+xml;base64," + base64.b64encode(app_icon.read_bytes()).decode("utf-8")

    manifest["readme"] = readme
    manifest["icon"] = icon
    manifest["source_hash"] = "sha256:" + hashlib.sha256(source.encode("utf-8")).hexdigest()
    manifest["source"] = source
    return manifest


def app_dry_run(manifest: Dict, config_path: str = None) -> None:
    env = Environment(extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"])
    template = env.from_string(manifest["source"])
    template.globals["parse_duration"] = parse_optional_duration

    if "search(" in manifest["source"]:
        tls_data: Optional[TLSData] = None
        if resotocore.is_secure:
            tls_data = TLSData(
                common_name=ArgumentParser.args.subscriber_id,
                resotocore_uri=resotocore.http_uri,
            )
            tls_data.start()
            tls_data.shutdown()
        cg = CoreGraph(tls_data=tls_data, graph="resoto")
        template.globals["search"] = cg.search

    if config_path is not None:
        config_path = Path(config_path)
        if not config_path.exists():
            raise RuntimeError(f"Path {config_path} does not exist")
        config = yaml.load(config_path.read_text(), Loader=yaml.FullLoader)
    else:
        config = manifest["default_config"]

    try:
        rendered_app = template.render(config=config)
        for command in rendered_app.splitlines():
            if not command or command.isspace():
                continue
            print(command)
    except Exception:
        log.exception("Failed to render app")
