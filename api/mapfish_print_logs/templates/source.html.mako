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
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
    crossorigin="anonymous">
  <link rel="stylesheet" href="/logs/style.css">
  <title>Mapfish print logs - ${source | h}</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
      <form class="form-inline mx-2 mb-0 float-right" role="form" action="/logs/source" method="post"
        enctype="application/x-www-form-urlencoded">
        <input type="hidden" name="source" value="${source | h}">
        <input type="hidden" name="key" value="${key | h}">
        <input type="hidden" name="pos" value="0">
        <button type="submit" class="btn btn-primary float-right">Refresh logs</button>
      </form>
      <h3 style="display: inline">Logs for ${source | h}</h3>
      <nav style="display: inline-block" class="ml-4">
        <ul class="pagination justify-content-center mb-0">
          <li class="page-item ${'disabled' if next_pos is None else ''}">
            <form class="form-inline mb-0" role="form" action="/logs/source" method="post"
              enctype="application/x-www-form-urlencoded">
              <input type="hidden" name="source" value="${source | h}">
              <input type="hidden" name="key" value="${key | h}">
              <input type="hidden" name="pos" value="${next_pos}">
              <button type="submit" class="page-link">older</button>
            </form>
          </li>
          <li class="page-item ${'disabled' if prev_pos is None else ''}">
            <form class="form-inline mb-0" role="form" action="/logs/source" method="post"
              enctype="application/x-www-form-urlencoded">
              <input type="hidden" name="source" value="${source | h}">
              <input type="hidden" name="key" value="${key | h}">
              <input type="hidden" name="pos" value="${prev_pos}">
              <button type="submit" class="page-link">younger</button>
            </form>
          </li>
        </ul>
      </nav>
    </div>
    <div class="card-body">

      <table class="table mb-0">
        <thead>
        <tr>
          <th scope="col">when</th>
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
                <a href="/logs/ref?ref=${job.reference_id | u}" target="_blank">
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
          <a class="btn btn-primary float-right" href="${scm_refresh_url}" target="_blank">Refresh config</a>
          <form class="form-inline mx-2 mb-0 float-right" role="form" action="/logs/source/accounting" method="post"
            enctype="application/x-www-form-urlencoded" target="_blank">
            <input type="hidden" name="source" value="${source | h}">
            <input type="hidden" name="key" value="${key | h}">
            <input type="hidden" name="pos" value="0">
            <button type="submit" class="btn btn-primary float-right">Accounting</button>
          </form>
        %endif
        <h3>Status for ${source | h}</h3>
      </div>
      <div class="card-body">
        %if 'status' in config:
          Error ${config['status'] | h}: ${config['message'] | h}
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

</body>
</html>
