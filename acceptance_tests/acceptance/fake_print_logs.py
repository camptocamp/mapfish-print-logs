import datetime
import os
import requests
import sys


ES_URL = os.environ['ES_URL']
INDEX = os.environ['ES_INDEX']


def _log_message(ref, level, message):
    data={
        'job_id': ref,
        '@timestamp': datetime.datetime.now().isoformat(),
        'level_name': level,
        'msg': message
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json"
    }
    r = requests.post(f"{ES_URL}/{INDEX}", json=data,
                      headers=headers)
    r.raise_for_status()


def gen_fake_print_logs(ref):
    _log_message(ref, 'INFO', f'Starting job {ref}')
    _log_message(ref, 'DEBUG', f'Some debug')
    _log_message(ref, 'WARN', f'Some warning')
    _log_message(ref, 'INFO', f'Finished job {ref} with some very long message')


def main():
    gen_fake_print_logs(sys.argv[1])


if __name__ == '__main__':
    main()
