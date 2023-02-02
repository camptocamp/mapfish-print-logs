import os
from typing import Any, Dict

import sqlalchemy as sa  # type: ignore
import sqlalchemy.ext.declarative  # type: ignore
from sqlalchemy.dialects.postgresql import JSONB  # type: ignore

from mapfish_print_logs import utils

Base = sqlalchemy.ext.declarative.declarative_base()
SCHEMA = os.environ.get("DB_SCHEMA", "public")


class PrintAccounting(Base):  # type: ignore
    __tablename__ = "print_accountings"
    __table_args__ = {"schema": SCHEMA}
    reference_id = sa.Column(sa.Text, primary_key=True)
    app_id = sa.Column(sa.Text, nullable=False)
    completion_time = sa.Column(sa.DateTime, nullable=False)
    file_size = sa.Column(sa.Integer)
    layout = sa.Column(sa.Text, nullable=False)
    mapexport = sa.Column(sa.Boolean, nullable=False)
    output_format = sa.Column(sa.Text, nullable=False)
    processing_time_ms = sa.Column(sa.Integer)
    referer = sa.Column(sa.Text)
    stats = sa.Column(JSONB)
    status = sa.Column(sa.Text, nullable=False)
    total_time_ms = sa.Column(sa.Integer)

    def to_json(self) -> Dict[str, Any]:
        return {
            "reference_id": self.reference_id,
            "app_id": self.app_id,
            "completion_time": self.completion_time.isoformat(),
            "file_size": self.file_size,
            "layout": self.layout,
            "map_export": self.mapexport,
            "output_format": self.output_format,
            "processing_time_ms": self.processing_time_ms,
            "referrer": self.referer,
            "stats": self.stats,
            "status": self.status,
            "total_time_ms": self.total_time_ms,
        }

    def pages_stats(self) -> str:
        if self.stats and "pages" in self.stats:
            stats = [utils.page_size2fullname(page) for page in self.stats["pages"]]
            summary: Dict[str, Any] = {}
            for stat in stats:
                summary.setdefault(stat, 0)
                summary[stat] += 1
            return "\n".join(f"{n}: {v}" for n, v in summary.items())
        return ""

    def maps_stats(self) -> str:
        if self.stats and "maps" in self.stats:
            # [{'dpi': 72.0, 'size': {'width': 780, 'height': 330}, 'nbLayers': 1}]
            maps = []
            for map_ in self.stats["maps"]:
                maps.append(
                    f'{map_["size"]["width"]}x{map_["size"]["height"]} D{int(map_["dpi"])} '
                    f'L{map_["nbLayers"]}'
                )
            return "\n".join(maps)
        return ""
