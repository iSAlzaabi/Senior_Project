import math
import traci


edges_id = ["A2B", "B2C", "C2D", "D2E", "F2G", "G2C"]

default_speed = 27.77
default_ramp_speed = 22.22
def_speed_kmh = math.ceil(default_speed*3.6)
def_ramp_speed_kmh = math.ceil(default_ramp_speed*3.6)

edges_speed_limits = [def_speed_kmh, def_speed_kmh, def_speed_kmh, def_speed_kmh, def_ramp_speed_kmh, def_ramp_speed_kmh]

congested_lane = "B2C_0"

def detect_lane_congestion(lane_id, density_threshold):
    veh_count = traci.lane.getLastStepVehicleNumber(lane_id)
    lane_length = traci.lane.getLength(lane_id)
    density = veh_count / lane_length
    return density > density_threshold


def update_speed(edge_id, new_speed):
    traci.edge.setMaxSpeed(edge_id, new_speed)
    # Specific for our implementation
    if edge_id == "A2B":
        edges_speed_limits[0] = math.ceil(new_speed*3.6)
    elif edge_id == "B2C":
        edges_speed_limits[1] = math.ceil(new_speed*3.6)
    elif edge_id == "C2D":
        edges_speed_limits[2] = math.ceil(new_speed*3.6)
    elif edge_id == "D2E":
        edges_speed_limits[3] = math.ceil(new_speed*3.6)
    elif edge_id == "F2G":
        edges_speed_limits[4] = math.ceil(new_speed*3.6)
    elif edge_id == "G2C":
        edges_speed_limits[4] = math.ceil(new_speed*3.6)


def default_state():
    # Specific for our implementation
    for i in range(4):
        traci.edge.setMaxSpeed(edges_id[i], default_speed)
        edges_speed_limits[i] = def_speed_kmh
    traci.edge.setMaxSpeed(edges_id[4], default_ramp_speed)
    traci.edge.setMaxSpeed(edges_id[5], default_ramp_speed)


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
        elif edge == "C2D":
            speed_limit = edges_speed_limits[2]
        elif edge == "D2E":
            speed_limit = edges_speed_limits[3]
        elif edge == "F2G":
            speed_limit = edges_speed_limits[4]
        elif edge == "G2C":
            speed_limit = edges_speed_limits[5]

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
    else:
        overall_avg_speed = 0

    if total_edges > 0:
        overall_avg_occupancy = total_occupancy / total_vehicle_count * 100
    else:
        overall_avg_occupancy = 0

    # Overall statistics
    statistics.append(f"Overall Avg Speed: {overall_avg_speed:.2f} km/h")
    statistics.append(f"Overall Vehicle Count: {total_vehicle_count}")
    statistics.append(f"Overall Network Occupancy: {overall_avg_occupancy:.2f}%")

    return "\n".join(statistics)


# Main simulation
traci.start(["sumo-gui", "-c", "simulation_files\highway.sumocfg"])

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    if detect_lane_congestion(congested_lane, 0.04):
        update_speed(edges_id[0], 16.66)
        update_speed(edges_id[1], 22.22)
        update_speed(edges_id[2], 33.33)
        update_speed(edges_id[3], 33.33)
        update_speed(edges_id[4], 25.0)
        update_speed(edges_id[5], 25.0)
    else:
        default_state()

    stats = get_edges_stats(edges_id)
    print(stats)

traci.close()