<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="style.css">
    <title>Mapfish print logs</title>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h3>Logs for one print job</h3>
        </div>
        <div class="card-body">
          <form role="form" action="ref">
            <div class="form-group row">
              <div class="col-lg-12">
                <label for="ref">Ref</label>
                <input id="ref" type="text" name="ref" class="form-control">
              </div>
            </div>
            <button type="submit" class="btn btn-primary float-right">Get</button>
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
                    <a role="button" class="btn btn-primary" href="/logs/source/${source['id'] | u}">
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
      %if is_admin:
        <a role="button" class="btn btn-primary mt-4 mr-3" href="/logs/accounting.csv">Accounting</a>
      %endif
      <a role="button" class="btn btn-secondary mt-4" href="/logs/logout">Logout</a>
      %else:
        <a role="button" class="btn btn-primary mt-4" href="/logs/login">Login</a>
      %endif

    </div>
  </body>
</html>
