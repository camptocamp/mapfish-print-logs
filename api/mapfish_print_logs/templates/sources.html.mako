<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
    crossorigin="anonymous">
  <link rel="stylesheet" href="/logs/style.css">
  <title>Mapfish print logs - All sources</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
      <form class="form-inline mx-2 mb-0 float-right" role="form" action="/logs/sources" method="post"
        enctype="application/x-www-form-urlencoded">
        <input type="hidden" name="key" value="${key | h}">
        <button type="submit" class="btn btn-primary float-right">Refresh</button>
      </form>
      <h3>List of sources</h3>
    </div>
    <div class="card-body">
      <table class="table">
        <thead>
        <tr>
          <th scope="col">Source</th>
          <th scope="col">Key</th>
          <th scope="col">Target dir</th>
          <th scope="col"></th>
        </tr>
        </thead>
        <tbody>
          %for source in sources:
            <tr>
              <td>
                ${source['id'] | h}
              </td>
              <td title="${source['key']}">
                ????
              </td>
              <td>${source.get('target_dir', source['id'])}</td>
              <td>
                <form class="form-inline mx-2 mb-0" role="form" action="/logs/source" method="post"
                  enctype="application/x-www-form-urlencoded">
                  <input type="hidden" name="source" value="${source['id'] | h}">
                  <input type="hidden" name="key" value="${source['key'] | h}">
                  <button type="submit" class="btn btn-primary btn-sm">View logs</button>
                </form>
              </td>
            </tr>
          %endfor
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
