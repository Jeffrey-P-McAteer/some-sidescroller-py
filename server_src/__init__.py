
# stdlib stuff
import os
import sys
import subprocess
import traceback
import socket

# try to import 3rd-party libs, installing w/ pip if they do not exist
try:
  import aiohttp.web
except:
  traceback.print_exc()
  subprocess.run([
    sys.executable, '-m', 'pip', 'install', '--user', 'aiohttp'
  ])
  import aiohttp.web

def get_lan_ip(outside_host_to_connect_to='1.1.1.1'):
  local_ip = None
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((outside_host_to_connect_to, 80))
    local_ip = s.getsockname()[0]
    s.close()
  except:
    traceback.print_exc()

  return local_ip

def getopt_val(args, opt_name, default_value):
  value = default_value
  for i in range(0, len(args) - 1):
    if args[i] == opt_name:
      value = args[i+1]
      # Also abuse the default to parse string value -> something commonly useful
      if isinstance(default_value, float):
        value = float(value)
      elif isinstance(default_value, int):
        value = int(value)

  return value

def main(args=sys.argv):
  print(f'args={args}')

  http_port = getopt_val(args, '--port', 8080)

  server = aiohttp.web.Application()

  server.add_routes([
    # aiohttp.web.get('/', http_index_req_handler),
    # aiohttp.web.get('/ws', ws_req_handler),
  ])

  # server.on_startup.append(start_background_tasks)
  # server.on_shutdown.append(stop_background_tasks)

  print()
  print(f'Listening on http://0.0.0.0:{http_port}/')
  print(f'local address is http://{get_lan_ip()}:{http_port}/')
  print()
  aiohttp.web.run_app(server, port=http_port)


