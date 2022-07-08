from typing import Any, Dict, Optional, Tuple, cast

import yaml

from mapfish_print_logs.config import SHARED_CONFIG_MASTER
from mapfish_print_logs.configuration import Config

PAGE_SIZE2NAME = {
    # taken from:
    # https://github.com/itext/itextpdf/blob/develop/itext/src/main/java/com/itextpdf/text/PageSize.java
    "420x595": "A5",
    "595x842": "A4",
    "842x1191": "A3",
    "1191x1684": "A2",
    "1684x2384": "A1",
    "2384x3370": "A0",
    "498x708": "B5",
    "708x1000": "B4",
    "1000x1417": "B3",
    "1417x2004": "B2",
    "2004x2834": "B1",
    "2834x4008": "B0",
    "283x416": "Postcard",
    "522x756": "Executive",
    "540x720": "Note",
    "612x792": "Letter",
    "612x1008": "Legal",
    "792x1224": "Tabloid",
}


def read_shared_config() -> Config:
    with open(SHARED_CONFIG_MASTER, encoding="utf-8") as file:
        config = cast(Dict[str, Any], yaml.load(file, Loader=yaml.SafeLoader))
    return cast(Config, config)


def page_size2fullname(dico: Dict[str, Any]) -> str:
    height, width = get_size(dico)
    size = "x".join(map(str, sorted([width, height])))
    return PAGE_SIZE2NAME.get(size, size) + (" portrait" if height > width else " landscape")


def get_size(dico: Dict[str, Any]) -> Tuple[int, int]:
    height = dico["height"]
    width = dico["width"]
    return height, width


def page_size2name(dico: Dict[str, Any]) -> str:
    height, width = get_size(dico)
    size = "x".join(map(str, sorted([width, height])))
    return cast(str, PAGE_SIZE2NAME.get(size, size))


def quote_like(text: str) -> str:
    return text.replace("%", r"\%").replace("_", r"\_")


def get_app_id(config: Config, source: str) -> str:
    source_config = config["sources"][source]
    return cast(str, source_config.get("app_id", source))


def app_id2source(app_id: str, config: Optional[Config] = None) -> str:
    app_id = app_id.split(":")[0]
    if config is None:
        config = read_shared_config()

    if app_id in config["sources"]:
        return app_id

    for source, source_config in config["sources"].items():
        if source_config.get("app_id") == app_id:
            return source

    return app_id
