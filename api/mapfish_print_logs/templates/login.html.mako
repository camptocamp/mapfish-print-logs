<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link rel="stylesheet" href="/logs/style.css">
  <title>Mapfish print logs - login</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
      <h3>Login</h3>
    </div>
    <div class="card-body">
      <form role="form" action="/logs/login" method="post"
        enctype="application/x-www-form-urlencoded">
        <input type="hidden" name="back" value="${back}">
        <div class="form-group row">
          <div class="col-sm-4 mx-auto">
            <input type="password" name="key" placeholder="key">
          </div>
        </div>
        <div class="form-group row">
          <div class="col-sm-4 mx-auto">
            <button type="submit" class="btn btn-lg btn-primary">Login</button>
            %if message:
              <div class="alert alert-danger mt-3">${message}</div>
            %endif
          </div>
        </div>
      </form>
    </div>
  </div>
</div>
</body>
</html>
