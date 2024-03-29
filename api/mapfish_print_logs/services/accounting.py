import csv
from typing import Any, Dict

import pyramid.request  # type: ignore
import pyramid.response  # type: ignore
from c2cwsgiutils import services
from pyramid.security import Denied  # type: ignore

from mapfish_print_logs import accounting, utils
from mapfish_print_logs.security import auth_source

accounting_service = services.create("accounting", "/source/{source}/accounting")
accounting_csv_service = services.create("accounting_csv", "/source/{source}/accounting.csv")
global_accounting_service = services.create("accounting_global", "/accounting.csv")


@accounting_service.get(renderer="../templates/accounting.html.mako")  # type: ignore
def get_accounting(request: pyramid.request.Request) -> Dict[str, Any]:
    config, source = auth_source(request)
    monthly = accounting.monthly(request, utils.get_app_id(config, source))
    return {
        "source": source,
        "accounting": monthly,
        "detail_cols": accounting.get_details_cols(monthly),
    }


@accounting_csv_service.get()  # type: ignore
def get_accounting_csv(request: pyramid.request.Request) -> pyramid.response.Response:
    config, source = auth_source(request)
    monthly = accounting.monthly(request, utils.get_app_id(config, source))
    details_cols = accounting.get_details_cols(monthly)
    request.response.content_type = "text/csv"
    writer = csv.writer(request.response.body_file)
    writer.writerow(["month", "cost"] + details_cols)
    for month in monthly:
        row = [month["month"], month["amount"]]
        for col in details_cols:
            row.append(month["details"].get(col, ""))
        writer.writerow(row)
    return request.response


@global_accounting_service.get()  # type: ignore
def global_accounting_csv(request: pyramid.request.Request) -> pyramid.response.Response:
    permission = request.has_permission("all", {})
    if isinstance(permission, Denied):
        raise pyramid.httpexceptions.HTTPForbidden(permission.msg)

    config = utils.read_shared_config()

    monthly = accounting.monthly_all(request, config)
    details_cols = accounting.get_details_cols(monthly)
    request.response.content_type = "text/csv"
    writer = csv.writer(request.response.body_file)
    writer.writerow(["month", "source", "cost"] + details_cols)
    for month in monthly:
        row = [month["month"], month["source"], month["amount"]]
        for col in details_cols:
            row.append(month["details"].get(col, ""))
        writer.writerow(row)
    return request.response
