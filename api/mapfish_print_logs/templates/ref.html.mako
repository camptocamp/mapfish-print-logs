<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link rel="stylesheet" href="style.css">
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
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
        <dd class="col-lg-4">${accounting.app_id | h}</dd>
        <dt class="col-lg-2">layout</dt>
        <dd class="col-lg-4">${accounting.layout | h}</dd>

        <dt class="col-lg-2">referer</dt>
        <dd class="col-lg-4">${accounting.referer | h}</dd>
        <dt class="col-lg-2">status</dt>
        <dd class="col-lg-4">${accounting.status | h}</dd>

        <dt class="col-lg-2">completion</dt>
        <dd class="col-lg-4">${accounting.completion_time | h}</dd>
        <dt class="col-lg-2">file size</dt>
        <dd class="col-lg-4">${accounting.file_size | h}</dd>

        <dt class="col-lg-2">processing time</dt>
        <dd class="col-lg-4">${accounting.processing_time_ms | h}ms</dd>
        <dt class="col-lg-2">total time</dt>
        <dd class="col-lg-4">${accounting.total_time_ms | h}ms</dd>

        <dt class="col-lg-2">output format</dt>
        <dd class="col-lg-4">${accounting.output_format | h}</dd>
        <dt class="col-lg-2">mapexport</dt>
        <dd class="col-lg-4">${accounting.mapexport | h}</dd>

      </dl>

      <table class="table">
        <thead>
          <tr>
            <th scope="col" style="width: 1rem;"></th>
            <th scope="col" style="width: 16rem;">When</th>
            <th scope="col" style="width: 6rem;">Level</th>
            <th scope="col">Message</th>
          </tr>
        </thead>
        <tbody>
          %for i, log in enumerate(logs):
          <tr class="level-${log['level_name'] | h}">
            <td><a data-toggle="collapse" href="#collapse-${i}">+</a></td>
            <td>${log['@timestamp'] | h}</td>
            <td>${log['level_name'] | h}</td>
            <td class="text-truncate">${log['msg'] | h}</td>
            <!-- TODO: show details -->
          </tr>
          <tr class="collapse multi-collapse" id="collapse-${i}">
            <td colspan="4">
              <dl class="border rounded row mx-1 bg-light">
                <dt class="col-lg-2">Message</dt>
                <dd class="col-lg-10">${log['msg'] | h}</dd>
                % if 'logger_name' in log:
                <dt class="col-lg-2">logger</dt>
                <dd class="col-lg-10">${log['logger_name'] | h}</dd>
                % endif
                % if 'thread_name' in log:
                  <dt class="col-lg-2">thread</dt>
                  <dd class="col-lg-10">${log['thread_name'] | h}</dd>
                % endif
                % if 'stack_trace' in log:
                <dt class="col-lg-2">stacktrace</dt>
                <dd class="col-lg-10"><pre>${log['stack_trace'] | h}</pre></dd>
                % endif
              </dl>
            </td>
          </tr>
          %endfor
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
