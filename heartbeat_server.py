from socket import *
import time
import sys

def serve(port, duration=180):  # Duration is set to 120 seconds (2 minutes)
    server_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
    server_socket.bind(('', port))  # Bind to the specified port
    server_socket.settimeout(10)  # Set a 10-second timeout
    print("Heartbeat server started...")

    received_packets = set()  # Store all received sequence numbers
    expected_packets = set(range(1, 11))  # Expected sequence numbers from 1 to 10
    start_time = time.time()  # Record the start time
    while True:
        # Check if the server has been running for more than the specified duration (2 minutes)
        if time.time() - start_time > duration:
            print("\nTime limit reached. Shutting down the server.")
            break  # Exit the loop after 2 minutes
        try:
            # Wait for incoming data from the client
            data, address = server_socket.recvfrom(1024)
            recv_time = time.time()  # Record the time the packet is received

            # Parse the received message
            message = data.decode().strip().split()
            seq, send_time = int(message[1]), float(message[2])

            # Store the received sequence number
            received_packets.add(seq)

            # Print received packet details
            print(f"Received heartbeat {seq} from {address} with latency: {recv_time - send_time:.6f} seconds")

        except timeout:
            # After 10 seconds of no packets, check for missing packets
            missing_packets = expected_packets - received_packets

            if missing_packets:
                print(f"No heartbeat detected for 10 seconds. Missing sequences: {sorted(missing_packets)}")
            else:
                print("All packets received successfully.")

            break  # Stop the server loop after timeout

        except KeyboardInterrupt:
            # Handle server interruption
            print("Server interrupted. Shutting down.")
            server_socket.close()
            sys.exit()

if __name__ == '__main__':
    # Start the server on port 12000
    serve(12000)
