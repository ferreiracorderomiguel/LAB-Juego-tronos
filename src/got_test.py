from got import *


def test_lee_batallas(batallas):
    print("1. test_lee_batallas")
    print(f"Primera batalla: {batallas[0]}")
    print(f"\nCuarta batalla: {batallas[3]}")
    print(f"\nÚltima batalla: {batallas[-1]}")

def test_reyes_mayor_menor_ejercito(reyes):
    print(f"\n2. test_reyes_mayor_menor_ejercito\n{reyes}")

def test_batallas_mas_comandantes(batallas):
    print(f"\n3. test_batallas_mas_comandantes:\n{batallas}")

if __name__ == "__main__":
    batallas = lee_batallas("data/battles.csv")
    # test_lee_batallas(batallas)
    # test_reyes_mayor_menor_ejercito(reyes_mayor_menor_ejercito(batallas))
    test_batallas_mas_comandantes(batallas_mas_comandantes(batallas, {'The North', 'The Riverlands'}, 4))