from . import elastic_search

from c2cwsgiutils import services

ref_service = services.create("ref", "/ref/{ref}")


@ref_service.get()
def get_ref(request):
    ref = request.matchdict.get('depth')
    return {
        'ref': ref,
        'logs': elastic_search.get_logs(ref)
    }
