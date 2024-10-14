from socket import *
import time
import random

def heartbeat(host, port, num_packets):
    client_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
    packets = [(seq, time.time()) for seq in range(1, num_packets + 1)]  # Create packet list

    # Simulate sending 60% of packets out of order
    out_of_order_count = int(0.6 * num_packets)  # Calculate 60% of total packets
    shuffled_packets = packets[:out_of_order_count]  # First 60% of packets
    remaining_packets = packets[out_of_order_count:]  # Remaining packets

    # Shuffle the first 60% to simulate out-of-order delivery
    random.shuffle(shuffled_packets)

    # Combine shuffled and remaining packets
    packets = shuffled_packets + remaining_packets

    try:
        for seq, send_time in packets:
            # Simulate 40% chance of dropping the packet
            if random.random() < 0.4:
                print(f"Dropped heartbeat {seq} (simulated packet loss).")
                continue  # Skip sending this packet

            # Prepare the message
            message = f"Heartbeat {seq} {send_time}"
            client_socket.sendto(message.encode(), (host, port))
            print(f"Sent heartbeat {seq} at {send_time:.6f}")

            # Wait 1 second before sending the next packet
            time.sleep(1)

    except KeyboardInterrupt:
        print("Client interrupted. Stopping heartbeats.")

    finally:
        # Close the socket after sending all packets
        client_socket.close()
        print("Heartbeat client stopped.")

if __name__ == '__main__':
    host = '127.0.0.1'  # Server IP address
    port = 12000  # Server port
    num_packets = 10  # Total number of packets to send

    # Start the heartbeat client
    heartbeat(host, port, num_packets)
