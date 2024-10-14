from socket import *
import time

def ping(host, port):
    """
    Sends 10 ping messages to the specified host and port.
    Collects responses and round-trip times (RTTs) for statistics.
    """
    resps = []  # To store responses and RTTs
    client_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
    client_socket.settimeout(1)  # Set 1-second timeout for responses

    # Send 10 ping messages with proper formatting
    for seq in range(1, 11):
        send_time = time.time()  # Record the time when the ping is sent
        message = f"{seq} Ping {send_time}"  # Prepare the ping message

        try:
            # Send the message to the server at the specified host and port
            client_socket.sendto(message.encode(), (host, port))

            # Receive the reply from the server
            data, server = client_socket.recvfrom(1024)
            recv_time = time.time()  # Record the time reply is received

            # Calculate the round-trip time (RTT)
            rtt = recv_time - send_time

            # Decode the server's reply
            server_reply = data.decode().strip()

            # Store the reply and RTT in the response list
            resps.append((seq, server_reply, rtt))

            # Print the server's reply and RTT
            print(f"Reply from server: {server_reply}, RTT: {rtt:.6f} seconds")

        except timeout:
            # If no reply is received within 1 second, consider it timed out
            print(f"Request timed out for sequence {seq}")
            # Append the timeout information to the responses list
            resps.append((seq, 'Request timed out', 0))

    # Close the socket after sending all pings
    client_socket.close()
    return resps

def compute_statistics(resps):
    """
    Compute and display statistics for the collected responses and RTTs.
    """
    # Filter out successful RTTs for statistics calculation
    rtts = [rtt for seq, reply, rtt in resps if reply != 'Request timed out']

    # Calculate packet loss percentage
    packet_loss = (1 - len(rtts) / 10) * 100

    # Display the ping statistics
    print("\nPing Statistics:")
    print(f"Packets: Sent = 10, Received = {len(rtts)}, Lost = {10 - len(rtts)} ({packet_loss:.1f}% loss)")

    # If there are successful pings, calculate RTT statistics
    if rtts:
        print(f"Minimum RTT: {min(rtts):.6f} seconds")
        print(f"Maximum RTT: {max(rtts):.6f} seconds")
        print(f"Average RTT: {sum(rtts) / len(rtts):.6f} seconds")

if __name__ == '__main__':
    # Ping the server on localhost at port 12000
    responses = ping('127.0.0.1', 12000)

    # Display the ping statistics after all pings are sent
    compute_statistics(responses)
