import math
from collections import defaultdict
from typing import Dict

from utils.io_utils import InData, OutData, Schedule
from .optimizer import Optimizer, Intersection


class OptimizerA(Optimizer):
    def solve(self, in_data: InData) -> OutData:
        streets_by_names = {street.name: street for street in in_data.streets}
        intersections: Dict[int, Intersection] = self.green_light_intersections(streets_by_names, in_data.vehicles)

        schedules = []

        for id, intersection in intersections.items():
            if len(intersection.incoming_streets_anytime) == 1:
                single_incoming_street = list(intersection.incoming_streets_anytime)[0]
                schedules.append(Schedule(i=id, E=1, streets_and_times=[(single_incoming_street, in_data.D)]))
            else:
                car_arrivals_sorted = sorted(intersection.cars_arrivals_at_intersection, key=lambda x: x.time)

                num_arrivals_per_street = defaultdict(int)
                for arrival in car_arrivals_sorted:
                    num_arrivals_per_street[arrival.incoming_street] += 1

                min_arrival_street = None
                min_arrival = math.inf
                for arrival in car_arrivals_sorted:
                    if num_arrivals_per_street[arrival.incoming_street] < min_arrival:
                        min_arrival_street = arrival.incoming_street
                        min_arrival = num_arrivals_per_street[arrival.incoming_street]

                streets_order_of_arrival = []
                for arrival in car_arrivals_sorted:
                    if arrival.incoming_street not in streets_order_of_arrival:
                        streets_order_of_arrival.append(arrival.incoming_street)
                    if len(streets_order_of_arrival) == len(intersection.incoming_streets_anytime):
                        break

                # if id == 499:
                #     streets_and_times = [(street_name, 1)
                #                          for street_name in streets_order_of_arrival]
                # else:
                #     streets_and_times = [(street_name, min(
                #         (num_arrivals_per_street[street_name] // num_arrivals_per_street[min_arrival_street]), in_data.D))
                #                          for street_name in streets_order_of_arrival]

                streets_and_times = [(street_name, min(
                    (num_arrivals_per_street[street_name] // num_arrivals_per_street[min_arrival_street]), 5))
                                     for street_name in streets_order_of_arrival]

                schedules.append(Schedule(i=id, E=len(streets_and_times), streets_and_times=streets_and_times))

        return OutData(A=len(schedules), schedules=schedules)
