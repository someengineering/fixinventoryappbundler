import yaml
from pathlib import Path
from jinja2 import Environment
from argparse import ArgumentParser, Namespace
from resotolib.logger import log
from resotolib.durations import parse_optional_duration
from resotolib.utils import stdin_generator
from resotolib.core.search import CoreGraph
from resotolib.core.ca import TLSData
from resotolib.core import add_args as core_add_args, resotocore
from resotolib.jwt import add_args as jwt_add_args
from typing import Dict, Optional, List, Type
from pydoc import locate


def add_args(arg_parser: ArgumentParser) -> None:
    TLSData.add_args(arg_parser)
    core_add_args(arg_parser)
    jwt_add_args(arg_parser)

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


def app_dry_run(manifest: Dict, config_path: str = None, argv: Optional[List[str]] = None) -> None:
    env = Environment(extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"])
    template = env.from_string(manifest["source"])
    template.globals["parse_duration"] = parse_optional_duration
    template.globals["stdin"] = stdin_generator()

    args = args_from_manifest(manifest, argv)
    template.globals["args"] = args

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


def args_from_manifest(manifest: Dict, argv: Optional[List[str]] = None) -> Namespace:
    args_schema = manifest.get("args_schema", {})

    parser = ArgumentParser(description=manifest.get("description"))

    def str_to_type(type_str: Optional[str] = None) -> Optional[Type]:
        if type_str is None:
            return None
        supported_types = {"bool", "str", "int", "float", "complex"}
        if type_str not in supported_types:
            raise ValueError(f"Unsupported type: {type_str}")
        return locate(type_str)

    for arg_name, arg_info in args_schema.items():
        help_text = arg_info.get("help")
        action = arg_info.get("action")
        default_value = arg_info.get("default")
        arg_type_str = arg_info.get("type")
        nargs = arg_info.get("nargs")
        required = arg_info.get("required")

        parser.add_argument(
            f"--{arg_name}",
            help=help_text,
            action=action,
            default=default_value,
            type=str_to_type(arg_type_str),
            nargs=nargs,
            required=required,
        )

    return parser.parse_args(argv)
