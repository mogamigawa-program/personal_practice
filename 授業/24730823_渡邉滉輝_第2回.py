import numpy as np
import random

def exponential_random(mean):
    """Generate random numbers following exponential distribution using inverse transform."""
    return -mean * np.log(1.0 - random.random())

def monte_carlo_serial(buffer_a, buffer_b, arrival_rate, service_mean, delay, num_packets=10**6, num_simulations=21):
    """
    Perform Monte Carlo simulation for serial communication network.
    
    Args:
        buffer_a (int): Buffer size of Node 1.
        buffer_b (int): Buffer size of Node 2.
        arrival_rate (float): Arrival rate (lambda).
        service_mean (float): Mean service time.
        delay (float): Propagation delay between Node 1 and Node 2.
        num_packets (int): Number of packets to simulate per run.
        num_simulations (int): Number of simulation runs.
    
    Returns:
        dict: Performance metrics with mean and 95% confidence intervals.
    """
    results = []

    for _ in range(num_simulations):
        # Initialize variables for simulation
        current_time = 0
        node1_buffer = []
        node2_buffer = []
        node2_arrival_time = []
        rejected_packets_node1 = 0
        rejected_packets_node2 = 0
        total_packets = 0
        total_delay = 0
        total_queue_delay = 0
        system_packets_node1 = 0
        system_packets_node2 = 0

        while total_packets < num_packets:
            # Generate inter-arrival time and service time
            inter_arrival_time = exponential_random(1 / arrival_rate)
            service_time = exponential_random(service_mean)

            current_time += inter_arrival_time
            total_packets += 1

            # Node 1 processing
            if len(node1_buffer) < buffer_a:
                node1_buffer.append((current_time, service_time))
            else:
                rejected_packets_node1 += 1

            # Process Node 1 buffer
            if node1_buffer:
                if current_time >= node1_buffer[0][0] + node1_buffer[0][1]:
                    packet = node1_buffer.pop(0)
                    node2_arrival_time.append(packet[0] + packet[1] + delay)

            # Node 2 processing
            if node2_arrival_time and node2_arrival_time[0] <= current_time:
                if len(node2_buffer) < buffer_b:
                    arrival_time = node2_arrival_time.pop(0)
                    node2_buffer.append((arrival_time, exponential_random(service_mean)))
                else:
                    rejected_packets_node2 += 1

            if node2_buffer:
                if current_time >= node2_buffer[0][0] + node2_buffer[0][1]:
                    packet = node2_buffer.pop(0)
                    delay_time = current_time - packet[0]
                    total_delay += delay_time
                    total_queue_delay += max(0, delay_time - service_mean)

            # Track system packets
            system_packets_node1 += len(node1_buffer)
            system_packets_node2 += len(node2_buffer)

        # Calculate performance metrics
        reject_rate_node1 = rejected_packets_node1 / total_packets
        reject_rate_node2 = rejected_packets_node2 / total_packets
        total_reject_rate = (rejected_packets_node1 + rejected_packets_node2) / total_packets

        avg_system_delay = total_delay / (total_packets - rejected_packets_node1 - rejected_packets_node2)
        avg_queue_delay = total_queue_delay / (total_packets - rejected_packets_node1 - rejected_packets_node2)

        avg_system_packets_node1 = system_packets_node1 / total_packets
        avg_system_packets_node2 = system_packets_node2 / total_packets
        avg_total_system_packets = (system_packets_node1 + system_packets_node2) / total_packets

        results.append({
            "reject_rate_node1": reject_rate_node1,
            "reject_rate_node2": reject_rate_node2,
            "total_reject_rate": total_reject_rate,
            "avg_system_delay": avg_system_delay,
            "avg_queue_delay": avg_queue_delay,
            "avg_system_packets_node1": avg_system_packets_node1,
            "avg_system_packets_node2": avg_system_packets_node2,
            "avg_total_system_packets": avg_total_system_packets,
        })

    # Aggregate results and compute confidence intervals
    metrics = {
        "reject_rate_node1": [],
        "reject_rate_node2": [],
        "total_reject_rate": [],
        "avg_system_delay": [],
        "avg_queue_delay": [],
        "avg_system_packets_node1": [],
        "avg_system_packets_node2": [],
        "avg_total_system_packets": []
    }
    for result in results:
        for key in metrics:
            metrics[key].append(result[key])

    output = {}
    for key, values in metrics.items():
        mean = np.mean(values)
        ci = 2.086 * np.std(values, ddof=1) / np.sqrt(num_simulations)
        output[key] = {"mean": mean, "95%_ci": (mean - ci, mean + ci)}

    return output

# Parameters
buffer_a = 10
buffer_b = 10
arrival_rate = 0.5
service_mean = 1
delay = 0.5

# Run simulation
results = monte_carlo_serial(buffer_a, buffer_b, arrival_rate, service_mean, delay)

# Print results
for metric, value in results.items():
    print(f"{metric.replace('_', ' ').capitalize()}: Mean = {value['mean']:.6f}, 95% CI = ({value['95%_ci'][0]:.6f}, {value['95%_ci'][1]:.6f})")
