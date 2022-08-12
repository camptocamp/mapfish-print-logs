from typing import Dict, Optional, TypedDict


class AuthConfig(TypedDict, total=False):
    github_repository: str
    github_access_type: str


class SourceConfig(TypedDict, total=False):
    name: str
    id: Optional[str]
    key: Optional[str]
    auth: AuthConfig


class Config(TypedDict, total=False):
    sources: Dict[str, SourceConfig]
