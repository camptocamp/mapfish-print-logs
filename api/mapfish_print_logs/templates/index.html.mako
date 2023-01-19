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
    <link
      rel="icon"
      type="image/png"
      sizes="32x32"
      href="${request.static_url('/app/mapfish_print_logs/static/favicon-32x32.png')}"
      referrerpolicy="no-referrer"
    />
    <link
      rel="icon"
      type="image/png"
      sizes="16x16"
      href="${request.static_url('/app/mapfish_print_logs/static/favicon-16x16.png')}"
      referrerpolicy="no-referrer"
    />
    <title>Mapfish print logs</title>
  </head>
  <body>
    <div class="container">
      <div class="card" style="margin-bottom: 1rem;">
        <div class="card-header">
          <h3>Logs for one print job</h3>
        </div>
        <div class="card-body">
          <form role="form" action="ref">
            <div class="form-group row">
              <div class="col-lg-12 input-group">
                <input id="ref" type="text" name="ref" class="form-control" placeholder="Ref" aria-label="Ref" aria-describedby="button-get">
                <button type="submit" class="btn btn-outline-primary" id="button-get">Get</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      %if sources:
      <div class="card">
        <div class="card-header">
          <h3>Logs for a source</h3>
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
            <tr>
              <th scope="col">Source</th>
              <th scope="col">App</th>
              <th scope="col"></th>
            </tr>
            </thead>
            <tbody>
              %for source in sources + ([{'id': 'all', 'app_id': 'All sources'}] if is_admin else []):
                <tr>
                  <td>
                    ${source['id'] | h}
                  </td>
                  <td>${source.get('app_id', source.get('target_dir', source['id']))}</td>
                  <td>
                    <a role="button" class="btn btn-primary" href="${request.route_url('source_auth', source=source['id'])}">
                      View
                    </a>
                  </td>
                </tr>
              %endfor
            </tbody>
          </table>
          %for source in sources:
          %endfor
        </div>
      </div>
      <div>
      %if request.identity.is_admin:
        <a role="button" class="btn btn-primary mt-4 mr-3" style="vertical-align: baseline;"
          href="${request.route_url('accounting_global')}">Accounting</a>
      %endif
      Logged as: <a href="${request.identity.url}">${request.identity.name}</a>, <a role="button"
        class="btn btn-secondary mt-4"
        style="vertical-align: baseline;"
        href="${request.route_url('c2c_github_logout', _query={'came_from': request.current_route_url()})}"
          >Logout</a>
      %else:
        <a class="btn btn-primary"
          href="${request.route_url('c2c_github_login', _query={'came_from': request.current_route_url()})}"
          >Login with GitHub</a>
      %endif
      </div>
    </div>
  </body>
</html>
