from abc import ABC, abstractmethod

from utils.io_utils import InData, OutData



class Optimizer(ABC):
    """
    This is an abstract class that represents an optimizer.
    All optimizers (naive, specific etc.) should inherit and implement it.
    Note: inheriting classes might also have some hyper-parameters set in the c'tor, for example.
    """

    @abstractmethod
    def solve(self, in_data: InData) -> OutData:
        pass

    @staticmethod
    def calc_score(solution: OutData, in_data: InData) -> float:
        # TODO: implement according to problem statement
        pass
