import yaml
import base64
import hashlib
from pathlib import Path
from resotolib.logger import log
from resotolib.args import ArgumentParser
from typing import Dict, List, Union


def add_args(arg_parser: ArgumentParser) -> None:
    arg_parser.add_argument(
        "--discover",
        help="Find all apps in the path",
        dest="discover",
        required=False,
        action="store_true",
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

    for key in [
        "name",
        "description",
        "version",
        "language",
        "license",
        "authors",
        "url",
        "categories",
        "default_config",
        "config_schema",
        "args_schema",
    ]:
        if key not in manifest:
            raise ValueError(f"Key {key} is missing from {app_manifest}")

    readme = app_readme.read_text()
    icon = "data:image/svg+xml;base64," + base64.b64encode(app_icon.read_bytes()).decode("utf-8")

    manifest["readme"] = readme
    manifest["icon"] = icon
    manifest["source_hash"] = "sha256:" + hashlib.sha256(source.encode("utf-8")).hexdigest()
    manifest["source"] = source
    return manifest
