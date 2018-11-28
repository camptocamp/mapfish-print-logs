from c2cwsgiutils import db
import sqlalchemy as sa
import sqlalchemy.ext.declarative
from sqlalchemy.dialects.postgresql import JSONB

DBSession = None
Base = sqlalchemy.ext.declarative.declarative_base()
PAGE_SIZE2NAME = {
    '420x595': 'A5',
    '595x842': 'A4',
    '842x1191': 'A3',
    '1191x1684': 'A2'
}


def init(config):
    global DBSession
    DBSession = db.setup_session(config, 'sqlalchemy')[0]


class PrintAccounting(Base):
    __tablename__ = "print_accountings"
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

    def to_json(self):
        return dict(
            reference_id=self.reference_id,
            app_id=self.app_id,
            completion_time=self.completion_time.isoformat(),
            file_size=self.file_size,
            layout=self.layout,
            map_export=self.mapexport,
            output_format=self.output_format,
            processing_time_ms=self.processing_time_ms,
            referer=self.referer,
            stats=self.stats,
            status=self.status,
            total_time_ms=self.total_time_ms
        )

    def pages_stats(self):
        if self.stats and 'pages' in self.stats:
            stats = [_page_size2name(page) for page in self.stats['pages']]
            summary = {}
            for stat in stats:
                summary.setdefault(stat, 0)
                summary[stat] += 1
            return '\n'.join(f'{n}: {v}' for n, v in summary.items())
        else:
            return ""

    def maps_stats(self):
        if self.stats and 'maps' in self.stats:
            # [{'dpi': 72.0, 'size': {'width': 780, 'height': 330}, 'nbLayers': 1}]
            maps = []
            for map in self.stats['maps']:
                maps.append(f'{map["size"]["width"]}x{map["size"]["height"]} D{int(map["dpi"])} L{map["nbLayers"]}')
            return '\n'.join(maps)
        else:
            return ""


def _page_size2name(dico):
    height = str(dico['height'])
    width = str(dico['width'])
    size = 'x'.join(sorted([width, height]))
    return PAGE_SIZE2NAME.get(size, size) + \
        (' portrait' if height > width else ' landscape')
