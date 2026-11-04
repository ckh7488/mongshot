"""Loopback-only, read-only serving of this one standalone workbench file."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import os,argparse
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=8766)
parser.add_argument('--pid-file')
args=parser.parse_args()
page=Path(__file__).resolve().parents[1]/'simulation/index.html'
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path not in ['/','/index.html','/simulation/index.html']:
            self.send_error(404);return
        data=page.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
server=HTTPServer(('127.0.0.1',args.port),Handler)
if args.pid_file:Path(args.pid_file).write_text(str(os.getpid()))
print(f'LOCAL_WORKBENCH_READY http://127.0.0.1:{args.port}',flush=True)
try:server.serve_forever()
finally:
    server.server_close()
    if args.pid_file:Path(args.pid_file).unlink(missing_ok=True)
