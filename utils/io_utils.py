from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Street:
    B: int  # intersection at the Beginning of the street
    E: int  # intersection at the End of the street
    name: str
    L: int  # time it takes for a car to cross the street


@dataclass
class Vehicle:
    P: int  # number of streets on its path
    streets_names: List[str]  # names of the streets on the path


@dataclass
class InData:
    # TODO: implement according to problem statement
    D: int  # duration of the simulation in seconds
    I: int  # number of intersections
    S: int  # number of streets
    V: int  # number of cars (vehicles)
    F: int  # bonus points for each car that reaches destination before D-day
    streets: List[Street]
    vehicles: List[Vehicle]


@dataclass
class Schedule:
    i: int  # the ID of the intersection
    E: int  # number of incoming streets in the schedule
    streets_and_times: List[Tuple[str, int]]  # for each street in the schedule store name and time it has a green light


@dataclass
class OutData:
    A: int  # number of intersections with schedule
    schedules: List[Schedule]


def read_input(in_filename: str) -> InData:
    with open(in_filename, 'r') as f:
        D, I, S, V, F = [int(_) for _ in f.readline().split()]
        streets = []
        vehicles = []

        for _ in range(S):
            line = f.readline().split()
            B = int(line[0])
            E = int(line[1])
            name = line[2]
            L = int(line[3])

            streets.append(Street(B=B, E=E, name=name, L=L))

        for _ in range(V):
            line = f.readline().split()
            P = int(line[0])
            streets_names = line[1:]

            vehicles.append(Vehicle(P=P, streets_names=streets_names))

        return InData(D=D, I=I, S=S, V=V, F=F, streets=streets, vehicles=vehicles)


def write_output(solution: OutData, out_filename):
    with open(out_filename, 'w') as f:
        f.write(str(solution.A) + '\n')

        for schedule in solution.schedules:
            f.write(str(schedule.i) + '\n')
            f.write(str(schedule.E) + '\n')

            for s, t in schedule.streets_and_times:
                f.write(f'{s} {t}\n')
