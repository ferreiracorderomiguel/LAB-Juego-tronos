from got import *


def test_lee_batallas(batallas):
    print("1. test_lee_batallas")
    print(f"Primera batalla: {batallas[0]}")
    print(f"\nCuarta batalla: {batallas[3]}")
    print(f"\nÚltima batalla: {batallas[-1]}")

if __name__ == "__main__":
    batallas = lee_batallas("data/battles.csv")
    test_lee_batallas(batallas)