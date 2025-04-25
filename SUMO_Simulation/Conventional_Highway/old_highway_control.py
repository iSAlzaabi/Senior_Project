import math
import traci


edges_id = ["A2B", "B2C", "E2F", "F2B"]

default_speed = 27.77
default_ramp_speed = 22.22
def_speed_kmh = math.ceil(default_speed*3.6)
def_ramp_speed_kmh = math.ceil(default_ramp_speed*3.6)

edges_speed_limits = [def_speed_kmh, def_speed_kmh, def_ramp_speed_kmh, def_ramp_speed_kmh]


def get_edges_stats(edges):
    statistics = []
    speed_limit = 0
    total_speed = 0
    total_vehicle_count = 0
    total_occupancy = 0
    total_edges = 0

    # Specific for our implementation
    for edge in edges:
        if edge == "A2B":
            speed_limit = edges_speed_limits[0]
        elif edge == "B2C":
            speed_limit = edges_speed_limits[1]
        elif edge == "E2F":
            speed_limit = edges_speed_limits[2]
        elif edge == "F2B":
            speed_limit = edges_speed_limits[3]

        mean_speed = traci.edge.getLastStepMeanSpeed(edge)*3.6
        veh_count = traci.edge.getLastStepVehicleNumber(edge)
        occupancy = traci.edge.getLastStepOccupancy(edge)

        # Add to the global totals for overall stats
        total_speed += mean_speed * veh_count
        total_vehicle_count += veh_count
        total_occupancy += occupancy * veh_count
        total_edges += 1

        statistics.append(
            f"{edge}: Max Speed: {speed_limit:.0f}km/h, Avg Speed: {mean_speed:.0f}km/h, Vehicle Count: {veh_count}, Edge Occupancy: {occupancy*100:.1f}%"
        )

    # Calculate overall average speed and occupancy for the edges
    if total_vehicle_count > 0:
        overall_avg_speed = total_speed / total_vehicle_count
        overall_avg_occupancy = total_occupancy / total_vehicle_count * 100
    else:
        overall_avg_speed = 0
        overall_avg_occupancy = 0

    # Overall statistics
    statistics.append(f"Overall Avg Speed: {overall_avg_speed:.2f} km/h")
    statistics.append(f"Overall Vehicle Count: {total_vehicle_count}")
    statistics.append(f"Overall Network Occupancy: {overall_avg_occupancy:.2f}%")

    return "\n".join(statistics)


# Main simulation
traci.start(["sumo-gui", "-c", "simulation_files\oldHighways.sumocfg"])

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    stats = get_edges_stats(edges_id)
    print(stats)

traci.close()