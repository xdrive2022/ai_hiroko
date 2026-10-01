# -*- coding: utf-8 -*-
"""ブラウザから Dify を直接呼べない（CORS）ときの中継。

    python3 proxy.py          # http://localhost:8788 で待ち受け

index.html の設定で API サーバーを http://localhost:8788/v1 にする。
APIキーはブラウザから来た Authorization をそのまま渡すだけで、ここには保存しない。
"""
import http.server
import urllib.request
import urllib.error

UPSTREAM = "https://api.dify.ai"
PORT = 8788


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(
            UPSTREAM + self.path, data=body, method="POST",
            headers={"Authorization": self.headers.get("Authorization", ""),
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as up:
                self.send_response(up.status)
                self._cors()
                self.send_header("Content-Type", up.headers.get("Content-Type", "application/json"))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                while True:                      # ストリーミングをそのまま流す
                    chunk = up.read(1)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"中継を開始しました → http://localhost:{PORT}/v1　（止めるには Ctrl+C）")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
