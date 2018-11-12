<%!
def render(value):
    if isinstance(value, str):
        return value
    else:
        return repr(value)
%>
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
  %if config is not None:
  <div class="card">
    <div class="card-header">
      %if scm_refresh_url is not None:
      <a class="btn btn-primary float-right" href="${scm_refresh_url}" target="_blank">Refresh config</a>
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
                <dt class="col-lg-1">${name | h}</dt>
                <dd class="col-lg-5">${render(value) | h}</dd>
              %endif
            %endfor
          </dl>
        %endfor
      %endif
    </div>
  </div>
  %endif

  <div class="card">
    <div class="card-header">
      <form class="form-inline mx-2 mb-0 float-right" role="form" action="/logs/source" method="post"
        enctype="application/x-www-form-urlencoded">
        <input type="hidden" name="source" value="${source | h}">
        <input type="hidden" name="key" value="${key | h}">
        <input type="hidden" name="pos" value="0">
        <button type="submit" class="btn btn-primary float-right">Refresh logs</button>
      </form>
      <h3>Logs for ${source | h}</h3>
    </div>
    <div class="card-body">
      <table class="table">
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
      <div>
        %if next_pos is not None:
          <form class="form-inline mr-2 mb-0" role="form" action="/logs/source" method="post"
            enctype="application/x-www-form-urlencoded">
            <input type="hidden" name="source" value="${source | h}">
            <input type="hidden" name="key" value="${key | h}">
            <input type="hidden" name="pos" value="${next_pos}">
            <button type="submit" class="btn btn-secondary float-right">older</button>
          </form>
        %endif
        %if prev_pos is not None:
          <form class="form-inline mr-2 mb-0" role="form" action="/logs/source" method="post"
            enctype="application/x-www-form-urlencoded">
            <input type="hidden" name="source" value="${source | h}">
            <input type="hidden" name="key" value="${key | h}">
            <input type="hidden" name="pos" value="${prev_pos}">
            <button type="submit" class="btn btn-secondary float-right">younger</button>
          </form>
        %endif
      </div>
    </div>
  </div>
</body>
</html>
