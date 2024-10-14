import random
from socket import *
import time
import hashlib
import sys

def serve(port):
    # Create a UDP socket (IPv4 + UDP)
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', port))  # Bind the socket to the specified port
    print(f"Server listening on port {port}")

    while True:
        try:
            # Simulate 30% packet loss with a random number
            rand = random.randint(0, 10)

            # Receive the client packet and address
            message, address = server_socket.recvfrom(1024)
            s_time = time.time()  # Server's receive time

            # Print the received message for debugging
            print(f"Received: {message.decode()} from {address}")

            # Simulate packet loss (skip sending response for 30% of packets)
            if rand < 4:
                print("Simulated packet loss.")
                continue

            # Parse the client message into sequence number, type, and timestamp
            m = message.decode().strip().split()
            if len(m) != 3:
                print(f"Invalid message format: {m}. Ignoring.")
                continue  # Ignore malformed messages

            seq = m[0]  # Sequence number (e.g., '9')
            ping_type = m[1]  # Type (should be 'Ping')
            c_time = m[2]  # Client's timestamp

            # Ensure the message type is 'Ping' to proceed
            if ping_type != "Ping":
                print(f"Unexpected message type: {ping_type}. Ignoring.")
                continue

            # Generate an MD5 message digest
            h = hashlib.md5(f"seq:{seq},c_time:{c_time},s_time:{s_time},key:randomkey".encode()).hexdigest()

            # Prepare the reply message
            resp = f"Reply {seq} {c_time} {s_time} {h}"

            # Send the reply to the client
            server_socket.sendto(resp.encode(), address)
            print(f"Sent: {resp}")

        except KeyboardInterrupt:  # Handle Ctrl+C gracefully
            print("\nServer shutting down.")
            server_socket.close()  # Close the socket and release resources
            sys.exit()
        except Exception as e:  # Handle other exceptions
            print(f"Error: {e}")
            continue

if __name__ == '__main__':
    # Start the server on port 12000
    serve(12000)
