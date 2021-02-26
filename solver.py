from pathlib import Path

from optimization.optimizer_a import OptimizerA
from utils.io_utils import read_input, write_output

IN_DATA_FOLDER = Path('data') / 'input'
OUT_DATA_FOLDER = Path('data') / 'output'
IN_SUFFIX = '.txt'
OUT_SUFFIX = '.out'

if __name__ == '__main__':
    in_files = ['a', 'b', 'c', 'd', 'e', 'f']  # TODO: implement according to files given (only names, no suffix)

    for f in in_files:
        in_filename = f + IN_SUFFIX
        out_filename = f + OUT_SUFFIX

        optimizer = OptimizerA()  # TODO: Optimizer is Abstract! change with a concrete one

        in_data = read_input(IN_DATA_FOLDER / in_filename)
        solution = optimizer.solve(in_data)
        # score = optimizer.calc_score(solution, in_data)
        # print(f'The score is: {score}')
        write_output(solution, OUT_DATA_FOLDER / out_filename)

    pass
