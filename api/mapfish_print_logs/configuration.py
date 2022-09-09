from typing import Dict, Optional, TypedDict

from c2cwsgiutils.auth import AuthConfig


class SourceConfig(TypedDict, total=False):
    name: str
    id: Optional[str]
    key: Optional[str]
    auth: AuthConfig


class Config(TypedDict, total=False):
    sources: Dict[str, SourceConfig]
