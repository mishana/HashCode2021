from dataclasses import dataclass
from typing import List, Tuple, Set

from .optimizer import Optimizer
from utils.io_utils import InData, OutData, Street, Schedule, Vehicle


@dataclass
class CarArrivalAtIntersection:
    time: int
    incoming_street: str
    score: int


@dataclass
class Intersection:
    incoming_streets_anytime: Set[str]
    outgoing_streets_anytime: Set[str]
    cars_arrivals_at_intersection: List[CarArrivalAtIntersection]


class OptimizerA(Optimizer):
    def solve(self, in_data: InData) -> OutData:
        streets_by_names = {street.name: street for street in in_data.streets}
        intersections = {}

        for vehicle in in_data.vehicles:
            T = 0
            for sn_from, sn_to in zip(vehicle.streets_names[:-1], vehicle.streets_names[1:]):
                # Here, the vehicle is at the intersection between street_from and street_to
                street_from = streets_by_names[sn_from]
                street_to = streets_by_names[sn_to]

                car_arrival = CarArrivalAtIntersection(time=T, incoming_street=sn_from, score=0)

                if street_from.E not in intersections:
                    intersections[street_from.E] = Intersection(incoming_streets_anytime={sn_from},
                                                                outgoing_streets_anytime={sn_to},
                                                                cars_arrivals_at_intersection=[car_arrival])
                else:
                    intersection = intersections[street_from.E]
                    intersection.incoming_streets_anytime.add(sn_from)
                    intersection.outgoing_streets_anytime.add(sn_to)
                    intersection.cars_arrivals_at_intersection.append(car_arrival)

                # advance the vehicle to the next intersection
                T += street_to.L

        pass

