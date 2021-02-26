from pathlib import Path

from optimization.optimizer_a import OptimizerA
from simulation.simulator import Simulator, SimulationResult
from utils.io_utils import read_input, write_output, InData

IN_DATA_FOLDER = Path('data') / 'input'
OUT_DATA_FOLDER = Path('data') / 'output'
IN_SUFFIX = '.txt'
OUT_SUFFIX = '.out'


def calc_score(simulation_result: SimulationResult, in_data: InData):
    return sum(in_data.F + (in_data.D - T) for T in simulation_result.finished_cars_times if T <= in_data.D)


if __name__ == '__main__':
    in_files = ['a', 'b', 'c', 'd', 'e', 'f']  # TODO: implement according to files given (only names, no suffix)

    for f in in_files:
        in_filename = f + IN_SUFFIX
        out_filename = f + OUT_SUFFIX

        optimizer = OptimizerA()  # TODO: Optimizer is Abstract! change with a concrete one

        in_data = read_input(IN_DATA_FOLDER / in_filename)
        solution = optimizer.solve(in_data)

        simulator = Simulator(in_data=in_data, solution=solution)
        simulation_result = simulator.simulate()

        score = calc_score(simulation_result, in_data)
        print(f'{in_filename}: The score is: {score}')
        write_output(solution, OUT_DATA_FOLDER / out_filename)

    pass
