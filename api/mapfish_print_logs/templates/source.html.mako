<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link rel="stylesheet" href="style.css">
  <title>Mapfish print logs - ${source | h}</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
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
                <a href="ref?ref=${job.reference_id | u}" target="_blank">
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
      <div class="row">
        <div class="mx-auto">
          %if next_pos is not None:
          <a href="source?source=${source | u}&pos=${next_pos}&key=${key | u}">
            older
          </a>
          %endif
          %if prev_pos is not None:
          <a href="source?source=${source | u}&pos=${prev_pos}&key=${key | u}">
            younger
          </a>
          %endif
        </div>
      </div>
    </div>
  </div>
</body>
</html>
