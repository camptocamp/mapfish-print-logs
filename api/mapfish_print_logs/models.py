from c2cwsgiutils import db
import sqlalchemy as sa
import sqlalchemy.ext.declarative
from sqlalchemy.dialects.postgresql import JSONB

DBSession = None
Base = sqlalchemy.ext.declarative.declarative_base()


def init(config):
    global DBSession
    DBSession = db.setup_session(config, 'sqlalchemy', 'sqlalchemy_slave')[0]


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
            completion_time=self.completion_time.isoformat(),
            file_size=self.file_size,
            layout=self.layout,
            map_export=self.mapexport,
            output_format=self.output_format,
            processing_time_ms=self.processing_time_ms,
            referer=self.referer,
            stats=self.stats,
            total_time_ms=self.total_time_ms
        )
