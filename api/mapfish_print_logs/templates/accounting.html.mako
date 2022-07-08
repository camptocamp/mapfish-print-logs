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
    <link rel="stylesheet" href="/logs/style.css">
    <title>Mapfish print logs - ${source | h} - accounting</title>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <div class="card-header">
          <a role="button" class="btn btn-primary float-right" href="/logs/source/${source | u}/accounting.csv">
            CSV
          </a>
          <h3 style="display: inline">Accounting for ${source | h}</h3>
        </div>
        <div class="card-body">
          <table class="table mb-0">
            <thead>
            <tr>
              <th scope="col">Month</th>
              <th scope="col">Cost</th>
              %for detail in detail_cols:
                <th scope="col">${detail}</th>
              %endfor
            </tr>
            </thead>
            <tbody>
              %for month in accounting:
                <tr>
                  <td>${month['month']}</td>
                  <td>${"%.02f" % (month['amount'])}</td>
                  %for detail in detail_cols:
                    <td>${month['details'].get(detail, 0)}</td>
                  %endfor
                </tr>
              %endfor
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </body>
</html>
