from collections import defaultdict
from typing import Dict, List, Optional

from dataclasses import dataclass

from utils.io_utils import OutData, InData, Vehicle, Street, Schedule


class TrafficLight:
    def __init__(self,
                 id: int,
                 schedule: Optional[Schedule],
                 cars_per_street: Dict[str, List[Vehicle]] = None):
        self.id = id

        # The vehicles are sorted for each street (first one is the closest)
        if cars_per_street is None:
            self.cars_per_street = defaultdict(list)
        else:
            self.cars_per_street = cars_per_street

        self.schedule = schedule

        if schedule is None:  # no schedule is provided for this traffic light
            self.current_street_name = None
        else:
            self.current_street_idx = 0
            self.current_street_name, self.current_timer = self.schedule.streets_and_times[self.current_street_idx]

    def advance_timer_one_sec(self):
        if self.schedule is None:  # no schedule is provided for this traffic light
            return

        self.current_timer -= 1

        if self.current_timer == 0:
            self.current_street_idx = (self.current_street_idx + 1) % len(self.schedule.streets_and_times)
            self.current_street_name, self.current_timer = self.schedule.streets_and_times[self.current_street_idx]


@dataclass
class SimulationResult:
    finished_cars_times: List[int]


class Simulator:
    def __init__(self, in_data: InData, solution: OutData):
        streets_by_names = {street.name: street for street in in_data.streets}
        schedules_by_id = {schedule.i: schedule for schedule in solution.schedules}

        # init traffic lights according to the schedules
        traffic_lights: Dict[int, TrafficLight] = {}
        for schedule in solution.schedules:
            traffic_lights[schedule.i] = TrafficLight(id=schedule.i, schedule=schedule)

        # init unscheduled traffic lights
        all_intersections_ids = {street.B for street in in_data.streets} | {street.E for street in in_data.streets}
        non_scheduled_intersections = all_intersections_ids - traffic_lights.keys()
        for traffic_light_id in non_scheduled_intersections:
            traffic_lights[traffic_light_id] = TrafficLight(id=traffic_light_id, schedule=None)

        # update traffic lights according to initial states of cars
        for vehicle in in_data.vehicles:
            start_street_name = vehicle.streets_names.pop(0)  # get start street name and advance the car across it
            start_street: Street = streets_by_names[start_street_name]

            traffic_light_id = start_street.E
            traffic_lights[traffic_light_id].cars_per_street[start_street_name].append(vehicle)

        self.traffic_lights = traffic_lights

        self.streets_by_names = streets_by_names
        self.schedules_by_id = schedules_by_id

        self.in_data = in_data
        self.solution = solution

    def simulate(self, simulation_time: int = None):
        if simulation_time is None:
            simulation_time = self.in_data.D

        finished_cars_times = []

        green_cars = []
        green_cars_time_on_the_street = []

        for T in range(simulation_time + 1):
            for traffic_light_id, traffic_light in self.traffic_lights.items():
                current_car_queue = traffic_light.cars_per_street[traffic_light.current_street_name]
                if current_car_queue and traffic_light.schedule is not None:
                    # advance the first car across the intersection
                    green_cars.append(current_car_queue.pop(0))
                    green_cars_time_on_the_street.append(0)

                traffic_light.advance_timer_one_sec()

            green_cars_finished_street_idxs = []

            for i, green_car in enumerate(green_cars):
                next_street: Street = self.streets_by_names[green_car.streets_names[0]]

                green_cars_time_on_the_street[i] += 1

                if len(green_car.streets_names) == 1:
                    finished_cars_times.append(T + next_street.L)

                    green_cars_finished_street_idxs.append(i)
                elif green_cars_time_on_the_street[i] >= next_street.L:
                    # get next street name and advance the car across it
                    green_car.streets_names.pop(0)

                    # add the car to the queue of the next traffic light
                    next_traffic_light_id = next_street.E
                    self.traffic_lights[next_traffic_light_id].cars_per_street[next_street.name].append(green_car)

                    green_cars_finished_street_idxs.append(i)

            for i in sorted(green_cars_finished_street_idxs, reverse=True):
                green_cars.pop(i)
                green_cars_time_on_the_street.pop(i)

        return SimulationResult(finished_cars_times=finished_cars_times)
