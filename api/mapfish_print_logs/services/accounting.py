from c2cwsgiutils import services
import csv
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest

from . import auth_source, SOURCES_KEY, read_shared_config
from .. import accounting, utils

global_accounting_service = services.create("accounting_global", "/logs/accounting.csv")
accounting_service = services.create("accounting", "/logs/source/accounting")
accounting_csv_service = services.create("accounting_csv", "/logs/source/accounting.csv")


@accounting_service.post(renderer='../templates/accounting.html.mako')
def get_accounting(request):
    config, key, source = auth_source(request)
    monthly = accounting.monthly(config, utils.get_app_id(config, source))
    return {
        'source': source,
        'key': key,
        'accounting': monthly,
        'detail_cols': accounting.get_details_cols(monthly)
    }


@accounting_csv_service.post()
def get_accounting_csv(request):
    config, key, source = auth_source(request)
    monthly = accounting.monthly(config, utils.get_app_id(config, source))
    details_cols = accounting.get_details_cols(monthly)
    request.response.content_type = "text/csv"
    writer = csv.writer(request.response.body_file)
    writer.writerow(['month', 'cost'] + details_cols)
    for month in monthly:
        row = [month['month'], month['amount']]
        for col in details_cols:
            row.append(month['details'].get(col, ''))
        writer.writerow(row)
    return request.response


@global_accounting_service.post()
def global_accounting_csv(request):
    key = request.params.get('key')
    if key is None:
        raise HTTPBadRequest("Missing the key")
    if key != SOURCES_KEY:
        raise HTTPForbidden("Invalid secret")
    config = read_shared_config()

    monthly = accounting.monthly_all(config)
    details_cols = accounting.get_details_cols(monthly)
    request.response.content_type = "text/csv"
    writer = csv.writer(request.response.body_file)
    writer.writerow(['month', 'source', 'cost'] + details_cols)
    for month in monthly:
        row = [month['month'], month['source'], month['amount']]
        for col in details_cols:
            row.append(month['details'].get(col, ''))
        writer.writerow(row)
    return request.response
