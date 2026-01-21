import sys
import time
import json

def ler_input():
    while True:
        linha = sys.stdin.readline()

        if linha == "":
            time.sleep(0.05)
            continue

        linha = linha.strip()
        if linha:
            return linha

""" O engine emite sempre json pra consumir """
def emit(tipo, payload=None):
    if payload is None:
        print(tipo, flush=True)
    else:
        print(f"{tipo}::{json.dumps(payload)}", flush=True)
