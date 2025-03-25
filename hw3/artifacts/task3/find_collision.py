from hw3 import Matrix
import copy
import numpy as np


def find_hash_collision():
    """Find matrices A and C with same hash but different values, and B == D where A@B != C@D"""
    size = 2
    attempts = 0
    max_attempts = 10000

    while attempts < max_attempts:
        attempts += 1
        A = Matrix.from_numpy(np.random.randint(0, 256, (size, size)))
        B = Matrix.from_numpy(np.random.randint(0, 256, (size, size)))
        C = Matrix.from_numpy(np.random.randint(0, 256, (size, size)))
        D = copy.deepcopy(B)

        if hash(A) == hash(C) and A != C:
            AB = A @ B
            CD = C @ D
            if AB != CD:
                A.to_file("tests/data/A.txt")
                B.to_file("tests/data/B.txt")
                C.to_file("tests/data/C.txt")
                D.to_file("tests/data/D.txt")
                AB.to_file("tests/data/AB.txt")
                CD.to_file("tests/data/CD.txt")

                with open("tests/data/hash.txt", "w") as f:
                    f.write(f"Hash of A and C: {hash(A)}\n")
                    f.write(f"Hash of AB: {hash(AB)}\n")
                    f.write(f"Hash of CD: {hash(CD)}\n")

                print(f"Found collision after {attempts} attempts")
                return True
    return False
