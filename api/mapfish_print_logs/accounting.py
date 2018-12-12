import sqlalchemy as sa

from . import utils
from .models import DBSession, PrintAccounting


PDF2M = 1/72 * 2.54/100

A4_SURFACE = 595 * 842


def monthly(config: dict, app_id: str):
    query = DBSession.query(PrintAccounting.completion_time, PrintAccounting.stats)\
        .filter(PrintAccounting.status == 'FINISHED',
                sa.or_(
                    PrintAccounting.app_id == app_id,
                    PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
                ))\
        .order_by(PrintAccounting.completion_time)
    a4price = config['accounting']['a4price']
    months = {}
    details = {}
    for completion_time, stats in query:
        month = f'{completion_time.year}/{completion_time.month}'
        amount = _compute_cost_cents(stats, a4price, details.setdefault(month, {}))
        if month not in months:
            months[month] = amount
        else:
            months[month] += amount
    return list({'month': k, 'amount': v/100, 'details': details[k]} for k, v in sorted(months.items()))


def _compute_cost_cents(stats, a4price, details):
    if stats is None or 'pages' not in stats:
        return 0
    pages = stats['pages']
    cost = 0
    for page in pages:
        height = page['height']
        width = page['width']
        cost += round(height * width / A4_SURFACE * a4price * 100)

        size_name = utils.page_size2name(page)
        if size_name not in details:
            details[size_name] = 1
        else:
            details[size_name] += 1

    return cost


def get_details_cols(months):
    cols = set()
    for month in months:
        cols |= month['details'].keys()
    return list(sorted(cols))
