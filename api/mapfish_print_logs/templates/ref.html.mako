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
        <dt class="col-lg-2">app ID</dt>
        <dd class="col-lg-4">${accounting.app_id}</dd>
        <dt class="col-lg-2">layout</dt>
        <dd class="col-lg-4">${accounting.layout}</dd>

        <dt class="col-lg-2">referer</dt>
        <dd class="col-lg-4">${accounting.referer}</dd>
        <dt class="col-lg-2">status</dt>
        <dd class="col-lg-4">${accounting.status}</dd>

        <dt class="col-lg-2">completion</dt>
        <dd class="col-lg-4">${accounting.completion_time}</dd>
        <dt class="col-lg-2">file size</dt>
        <dd class="col-lg-4">${accounting.file_size}</dd>

        <dt class="col-lg-2">processing time</dt>
        <dd class="col-lg-4">${accounting.processing_time_ms}ms</dd>
        <dt class="col-lg-2">total time</dt>
        <dd class="col-lg-4">${accounting.total_time_ms}ms</dd>

        <dt class="col-lg-2">output format</dt>
        <dd class="col-lg-4">${accounting.output_format}</dd>
        <dt class="col-lg-2">mapexport</dt>
        <dd class="col-lg-4">${accounting.mapexport}</dd>

      </dl>

      <table class="table">
        <thead>
          <tr>
            <th scope="col" style="width: 16rem;">When</th>
            <th scope="col" style="width: 6rem;">Level</th>
            <th scope="col">Message</th>
          </tr>
        </thead>
        <tbody>
          %for log in logs:
          <tr class="level-${log['level_name']}">
            <td>${log['@timestamp']}</td>
            <td>${log['level_name']}</td>
            <td class="text-truncate">${log['msg']}</td>
            <!-- TODO: show details -->
          </tr>
          %endfor
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
