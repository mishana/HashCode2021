from dataclasses import dataclass
from typing import List


@dataclass
class InData:
    # TODO: implement according to problem statement
    # Header Line
    M: int  # max num of slices
    N: int  # the number of different types of pizza
    slices_per_type: List[int]
    pass


@dataclass
class OutData:
    # TODO: implement according to problem statement
    K: int  # the number of different types of pizza to order
    types_to_order: List[int]


def read_input(in_filename: str) -> InData:
    # TODO: implement according to problem statement
    with open(in_filename, 'r') as myfile:
        M, N = [int(_) for _ in myfile.readline().split()]
        slices_per_type = [int(_) for _ in myfile.readline().split()]
        return InData(M=M, N=N, slices_per_type=slices_per_type)


def write_output(solution: OutData, out_filename):
    # TODO: implement according to problem statement
    with open(out_filename, 'w') as myfile:
        myfile.write(str(solution.K))
        myfile.write('\n')
        myfile.write(' '.join(map(str, solution.types_to_order)))


if __name__ == '__main__':
    from pathlib import Path

    data = read_input(Path('..') / 'example')
    print(data)
    out = OutData(K=2, types_to_order=[0, 1])
    out_filename = Path('..') / 'outfile'
    write_output(out, out_filename)

