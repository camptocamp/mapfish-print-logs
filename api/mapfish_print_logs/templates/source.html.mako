<%!
  def render(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, list):
        return "\n".join(render(i) for i in value)
    else:
        return repr(value)

  def dt_render(value):
    return value.replace("_", " ")
%>
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css"
        integrity="sha512-GQGU0fMMi238uA+a/bdWJfpUGKUkBdgfFdgBm72SUQ6BeyWjoY/ton0tEjH+OSH9iP4Dfh+7HM0I9f5eR0L/4w=="
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
    />
    <link rel="stylesheet" href="${request.static_url('/app/mapfish_print_logs/static/style.css')}">
    <title>Mapfish print logs - ${source | h}</title>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <div class="card-header">
          <a role="button" class="btn btn-primary float-right" href="${request.route_url('source_auth', source=source)}">
            Refresh
          </a>
          <a role="button" class="btn btn-secondary float-right mr-2"
            href="${request.route_url('source_auth', source=source, _query={'only_errors': '0' if only_errors else '1'})}">
            %if only_errors:
              Show all
            %else:
              Show only errors
            %endif
          </a>

          <a class="btn btn-secondary float-right mr-2" href="${request.route_url('index')}">Back to sources</a>
          <h3 style="display: inline">Logs for ${source | h}</h3>
          <nav style="display: inline-block" class="ml-4">
            <ul class="pagination justify-content-center mb-0">
              <li class="page-item ${'disabled' if next_pos is None else ''}">
                <a role="button" class="page-link" href="${request.route_url('source_auth', source=source, _query={'pos': next_pos})}">
                  older
                </a>
              </li>
              <li class="page-item ${'disabled' if prev_pos is None else ''}">
                <a role="button" class="page-link" href="${request.route_url('source_auth', source=source, _query={'pos': prev_pos})}">
                  younger
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <div class="card-body">
          <table class="table mb-0">
            <thead>
            <tr>
              <th scope="col">When</th>
              <th scope="col">Status</th>
              <th scope="col">App ID</th>
              <th scope="col">Layout</th>
              <th scope="col">Referer</th>
            </tr>
            </thead>
            <tbody>
              %for job in jobs:
                <tr>
                  <td>
                    <a href="${request.route_url('ref', _query={'ref': job.reference_id})}">
                      ${job.completion_time.isoformat().split('.')[0] | h}
                    </a>
                  </td>
                  <td class="job-${job.status}">${job.status | h}</td>
                  <td>${job.app_id | h}</td>
                  <td>${job.layout | h}</td>
                  <td class="text-truncate">${job.referer | h}</td>
                </tr>
              %endfor
            </tbody>
          </table>
        </div>
      </div>

      %if config is not None:
        <div class="card mt-8">
          <div class="card-header">
            %if scm_refresh_url is not None:
              <a class="btn btn-primary float-right" href="${request.route_url('accounting', source=source)}">
                Accounting
              </a>
              <a class="btn btn-secondary float-right mr-2" href="${scm_refresh_url}" target="_blank">
                Force refresh config
              </a>
            %endif
            <h3>Source config for ${source | h}</h3>
          </div>
          <div class="card-body">
            %if 'status' in config:
            <div class="alert alert-warning" role="alert">
              Error ${config['status'] | h}: ${config['message'] | h}
            </div>
            %else:
              %for status in config['statuses']:
                <dl class="border rounded row mx-1 bg-light mb-0">

                  %for name, value in status.items():
                    %if value:
                      <dt class="col-lg-2">${dt_render(name) | h}</dt>
                      <dd class="col-lg-10">${render(value) | h}</dd>
                    %endif
                  %endfor
                </dl>
              %endfor
            %endif
          </div>
        </div>
      %endif
    </div>
  </body>
</html>
