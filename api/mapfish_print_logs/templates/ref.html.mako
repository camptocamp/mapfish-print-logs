<%!
  import humanfriendly
%>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link rel="stylesheet" href="/logs/style.css">
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  <title>Mapfish print logs - ref</title>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="card-header">
      %if min_level > 10000:
      <a class="btn btn-primary float-right" href="ref?ref=${ref}&min_level=10000">Show debug</a>
      %else:
      <a class="btn btn-primary float-right" href="ref?ref=${ref}&min_level=20000">Hide debug</a>
      %endif
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

        <dt class="col-lg-2">output format</dt>
        <dd class="col-lg-4">${accounting.output_format | h}</dd>
        <dt class="col-lg-2">mapexport</dt>
        <dd class="col-lg-4">${accounting.mapexport | h}</dd>

        <dt class="col-lg-2">completion</dt>
        <dd class="col-lg-4">${accounting.completion_time | h}</dd>
        <dt class="col-lg-2">total time</dt>
        <dd class="col-lg-4">${accounting.total_time_ms / 1000.0 | h}s</dd>

        %if accounting.status == 'FINISHED':
        <dt class="col-lg-2">file size</dt>
        <dd class="col-lg-4">${humanfriendly.format_size(accounting.file_size, binary=True) | h}</dd>
        <dt class="col-lg-2">processing time</dt>
        <dd class="col-lg-4">${accounting.processing_time_ms / 1000.0 | h}s</dd>

        <dt class="col-lg-2">pages</dt>
        <dd class="col-lg-4">${accounting.pages_stats() | h}</dd>
        <dt class="col-lg-2">maps</dt>
        <dd class="col-lg-4">${accounting.maps_stats() | h}</dd>
        %endif

        %if accounting.stats is not None and 'emails' in accounting.stats:
          <dt class="col-lg-2">email</dt>
          <dd class="col-lg-4">${'\n'.join(dest['dest'] for dest in accounting.stats['emails']['dests']) | h}</dd>
          <dt class="col-lg-2">storage</dt>
          <dd class="col-lg-4">${accounting.stats['emails']['storageUsed'] | h}</dd>
        %endif
      </dl>

      %if len(logs) > 0:
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
          </tr>
          <tr class="collapse multi-collapse" id="collapse-${i}">
            <td colspan="4">
              <dl class="border rounded row mx-1 bg-light">
                <dt class="col-lg-2">Message</dt>
                <dd class="col-lg-10"><pre>${log['msg'] | h}</pre></dd>
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
      %else:
      <div class="alert alert-warning" role="alert">
        <p>No log found. This can happen for two reasons:</p>
        <ul>
          <li>
            The logs take some time to be processed.
          </li>
          <li>
            The logs are kept for a limited time. Maybe this job is too old.
          </li>
        </ul>
      </div>
      %endif
      <nav>
        <ul class="pagination justify-content-center">
          <li class="page-item ${'disabled' if prev_pos is None else ''}">
            <a class="page-link" href="ref?ref=${ref}&min_level=${min_level}&pos=0">
              &lt;&lt;
            </a>
          </li>
          <li class="page-item ${'disabled' if prev_pos is None else ''}">
            <a class="page-link" href="ref?ref=${ref}&min_level=${min_level}&pos=${prev_pos}">
              &lt;
            </a>
          </li>
          %for i, pos in enumerate(range(0, total, limit)):
          <li class="page-item ${'active' if pos == cur_pos else ''}">
            <a class="page-link" href="ref?ref=${ref}&min_level=${min_level}&pos=${pos}">
              ${i}
            </a>
          </li>
          %endfor
          <li class="page-item ${'disabled' if next_pos is None else ''}">
            <a class="page-link" href="ref?ref=${ref}&min_level=${min_level}&pos=${next_pos}">
              &gt;
            </a>
          </li>
          <li class="page-item ${'disabled' if last_pos is None else ''}">
            <a class="page-link" href="ref?ref=${ref}&min_level=${min_level}&pos=${last_pos}">
              &gt;&gt;
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</body>
</html>
