import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import http.cookiejar

READ_METHODS = {"web_search_read", "web_read_group", "read", "name_get"}
MODEL_METHODS = {
    "res.partner": READ_METHODS,
    "crm.lead": READ_METHODS,
    "sale.order": READ_METHODS,
    "sale.order.line": READ_METHODS,
    "kview.order.payment.collection.line": READ_METHODS,
    "product.template": READ_METHODS,
    "product.pricelist": READ_METHODS,
    "sale.report": {"web_read_group"},
    "crm.tag": {"read", "name_get"},
    "account.tax": {"read", "name_get"},
}

class OdooReadClient:
    def __init__(self):
        self.base = os.environ.get("ODOO_URL", "").rstrip("/")
        self.db = os.environ.get("ODOO_DB", "")
        self.login = os.environ.get("ODOO_LOGIN", "")
        self.password = os.environ.get("ODOO_PASSWORD", "")
        if not self.base or not self.db or not self.login or not self.password:
            raise RuntimeError("Set ODOO_URL, ODOO_DB, ODOO_LOGIN, and ODOO_PASSWORD")
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.counter = 0

    def call(self, path, params):
        self.counter += 1
        body = json.dumps({"jsonrpc": "2.0", "method": "call", "params": params, "id": self.counter}).encode()
        req = urllib.request.Request(self.base + path, data=body, headers={"Content-Type": "application/json"})
        try:
            with self.opener.open(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Odoo HTTP {exc.code}") from exc
        if result.get("error"):
            raise RuntimeError(json.dumps(result["error"], ensure_ascii=False))
        return result.get("result")

    def authenticate(self):
        return self.call("/web/session/authenticate", {"db": self.db, "login": self.login, "password": self.password})

    def read(self, model, method, args, kwargs):
        if model not in MODEL_METHODS or method not in MODEL_METHODS[model]:
            raise RuntimeError(f"Read method not allowlisted: {model}/{method}")
        return self.call(f"/web/dataset/call_kw/{model}/{method}", {"model": model, "method": method, "args": args, "kwargs": kwargs})

def main():
    parser = argparse.ArgumentParser(description="Read-only Odoo sales JSON-RPC client")
    parser.add_argument("command", choices=["auth", "call"])
    parser.add_argument("payload", nargs="?", default="{}", help="JSON payload")
    ns = parser.parse_args()
    client = OdooReadClient()
    client.authenticate()
    if ns.command == "auth":
        print(json.dumps({"authenticated": True}, ensure_ascii=False))
        return
    request = json.loads(ns.payload)
    result = client.read(request["model"], request["method"], request.get("args", []), request.get("kwargs", {}))
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
