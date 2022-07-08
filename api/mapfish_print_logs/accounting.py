import os
from typing import Any, Dict, List, Optional, Set, TypedDict, cast

import pyramid.request  # type: ignore
import sqlalchemy as sa  # type: ignore

from mapfish_print_logs import utils
from mapfish_print_logs.configuration import Config
from mapfish_print_logs.models import PrintAccounting

PDF2M = 1 / 72 * 2.54 / 100
A4_SURFACE = 595 * 842


def _add_dict(dico: Dict[str, Any], key: str, value: int = 1) -> None:
    if key in dico:
        dico[key] += value
    else:
        dico[key] = value


class Month(TypedDict, total=False):
    source: Optional[str]
    month: str
    amount: float
    details: Dict[str, str]


def monthly_all(request: pyramid.request.Request, config: Config) -> List[Month]:
    query = request.dbsession.query(
        PrintAccounting.app_id, PrintAccounting.completion_time, PrintAccounting.stats
    ).filter(PrintAccounting.status == "FINISHED")
    a4price = float(os.environ["PRINT_A4PRICE"])
    months: Dict[str, Dict[str, float]] = {}
    details: Dict[str, Dict[str, Dict[str, str]]] = {}
    for app_id, completion_time, stats in query:
        month = f"{completion_time.year}/{completion_time.month:02d}"
        source = utils.app_id2source(app_id, config)
        amount = _compute_cost_cents(stats, a4price, details.setdefault(month, {}).setdefault(source, {}))
        _add_dict(months.setdefault(month, {}), source, amount)
    return [
        {"source": source, "month": month, "amount": amount / 100.0, "details": details[month][source]}
        for month, sources in sorted(months.items())
        for source, amount in sorted(sources.items())
    ]


def monthly(request: pyramid.request.Request, app_id: str) -> List[Month]:
    query = request.dbsession.query(PrintAccounting.completion_time, PrintAccounting.stats).filter(
        PrintAccounting.status == "FINISHED",
        sa.or_(
            PrintAccounting.app_id == app_id, PrintAccounting.app_id.like(utils.quote_like(app_id) + ":%")
        ),
    )
    a4price = float(os.environ["PRINT_A4PRICE"])
    months: Dict[str, float] = {}
    details: Dict[str, Dict[str, str]] = {}
    for completion_time, stats in query:
        month = f"{completion_time.year}/{completion_time.month:02d}"
        amount = _compute_cost_cents(stats, a4price, cast(Dict[str, Any], details.setdefault(month, {})))
        _add_dict(months, month, amount)
    return [{"month": k, "amount": v / 100.0, "details": details[k]} for k, v in sorted(months.items())]


def _compute_cost_cents(stats: Dict[str, Any], a4price: float, details: Dict[str, str]) -> int:
    if stats is None or "pages" not in stats:
        return 0
    pages = stats["pages"]
    cost = 0
    for page in pages:
        height, width = utils.get_size(page)
        cost += round(height * width / A4_SURFACE * a4price * 100.0)

        size_name = utils.page_size2name(page)
        _add_dict(details, size_name)

    return cost


def get_details_cols(months: List[Month]) -> List[str]:
    cols: Set[str] = set()
    for month in months:
        cols |= month["details"].keys()
    return list(sorted(cols))
