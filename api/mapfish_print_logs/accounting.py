import sqlalchemy as sa

from . import utils
from .models import DBSession, PrintAccounting


PDF2M = 1/72 * 2.54/100
A4_SURFACE = 595 * 842


def _add_dict(dico: dict, key: str, value=1):
    if key in dico:
        dico[key] += value
    else:
        dico[key] = value


def monthly_all(config: dict):
    query = DBSession.query(PrintAccounting.app_id, PrintAccounting.completion_time, PrintAccounting.stats) \
        .filter(PrintAccounting.status == 'FINISHED')
    a4price = config['accounting']['a4price']
    months = {}
    details = {}
    for app_id, completion_time, stats in query:
        month = f'{completion_time.year}/{completion_time.month:02d}'
        source = utils.app_id2source(config, app_id)
        amount = _compute_cost_cents(stats, a4price, details.setdefault(month, {}).setdefault(source, {}))
        _add_dict(months.setdefault(month, {}), source, amount)
    return list({'source': source, 'month': month, 'amount': amount / 100.0, 'details': details[month][source]}
                for month, sources in sorted(months.items()) for source, amount in sorted(sources.items()))


def monthly(config: dict, app_id: str):
    query = DBSession.query(PrintAccounting.completion_time, PrintAccounting.stats) \
        .filter(PrintAccounting.status == 'FINISHED',
                sa.or_(
                    PrintAccounting.app_id == app_id,
                    PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
                ))
    a4price = config['accounting']['a4price']
    months = {}
    details = {}
    for completion_time, stats in query:
        month = f'{completion_time.year}/{completion_time.month:02d}'
        amount = _compute_cost_cents(stats, a4price, details.setdefault(month, {}))
        _add_dict(months, month, amount)
    return list({'month': k, 'amount': v / 100.0, 'details': details[k]} for k, v in sorted(months.items()))


def _compute_cost_cents(stats, a4price, details):
    if stats is None or 'pages' not in stats:
        return 0
    pages = stats['pages']
    cost = 0
    for page in pages:
        height, width = utils.get_size(page)
        cost += round(height * width / A4_SURFACE * a4price * 100.0)

        size_name = utils.page_size2name(page)
        _add_dict(details, size_name)

    return cost


def get_details_cols(months):
    cols = set()
    for month in months:
        cols |= month['details'].keys()
    return list(sorted(cols))
