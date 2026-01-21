import sys
import io
import argparse
from engine import run_game


def configurar_encoding():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome")
    parser.add_argument("--classe")
    args = parser.parse_args()

    run_game(
        nome_inicial=args.nome,
        classe_inicial=args.classe
    )


if __name__ == "__main__":
    configurar_encoding()
    main()
