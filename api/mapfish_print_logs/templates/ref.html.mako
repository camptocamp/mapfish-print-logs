<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link rel="stylesheet" href="style.css">
  <title>Mapfish print logs - ref</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
      <h3>Logs for one print job</h3>
      <small>${ref}</small>
    </div>
    <div class="card-body">
      <dl class="border rounded row mx-1 bg-light">
        <dt class="col-lg-2">app_id</dt>
        <dd class="col-lg-4">${accounting.app_id}</dd>
        <dt class="col-lg-2">completion_time</dt>
        <dd class="col-lg-4">${accounting.completion_time}</dd>

        <dt class="col-lg-2">file_size</dt>
        <dd class="col-lg-4">${accounting.file_size}</dd>
        <dt class="col-lg-2">layout</dt>
        <dd class="col-lg-4">${accounting.layout}</dd>

        <dt class="col-lg-2">mapexport</dt>
        <dd class="col-lg-4">${accounting.mapexport}</dd>
        <dt class="col-lg-2">output_format</dt>
        <dd class="col-lg-4">${accounting.output_format}</dd>

        <dt class="col-lg-2">referer</dt>
        <dd class="col-lg-4">${accounting.referer}</dd>
        <dt class="col-lg-2">status</dt>
        <dd class="col-lg-4">${accounting.status}</dd>

        <dt class="col-lg-2">processing_time</dt>
        <dd class="col-lg-4">${accounting.processing_time_ms}ms</dd>
        <dt class="col-lg-2">total_time</dt>
        <dd class="col-lg-4">${accounting.total_time_ms}ms</dd>
      </dl>

      <table class="table">
        <thead>
          <tr>
            <th scope="col">when</th>
            <th scope="col">level</th>
            <th scope="col">message</th>
          </tr>
        </thead>
        <tbody>
          %for log in logs:
          <tr>
            <td>${log['@timestamp']}}</td>
            <td>${log['level_name']}}</td>
            <td class="text-truncate">${log['msg']}}</td>
          </tr>
          %endfor
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
