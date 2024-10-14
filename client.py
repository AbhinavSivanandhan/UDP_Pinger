from socket import *
import time

def ping(host, port):
    # List to store responses and RTTs
    resps = []
    client_socket = socket(AF_INET, SOCK_DGRAM)  # Create UDP socket
    client_socket.settimeout(1)  # Set 1-second timeout for responses

    # Send 10 ping messages
    for seq in range(1, 11):
        # Record the send time
        send_time = time.time()
        # Prepare the ping message in the correct format
        message = f"{seq} Ping {send_time}"

        try:
            # Send the message to the server
            client_socket.sendto(message.encode(), (host, port))

            # Receive the reply from the server
            data, server = client_socket.recvfrom(1024)
            recv_time = time.time()  # Record the time reply is received

            # Calculate RTT
            rtt = recv_time - send_time
            server_reply = data.decode().strip()  # Decode server's response

            # Store the reply and RTT in the response list
            resps.append((seq, server_reply, rtt))
            print(f"Reply from server: {server_reply}, RTT: {rtt:.6f} seconds")

        except timeout:
            # If no reply is received within 1 second, consider it timed out
            print(f"Request timed out for sequence {seq}")
            resps.append((seq, 'Request timed out', 0))

    # Close the socket after sending all pings
    client_socket.close()
    return resps

def compute_statistics(resps):
    # Filter successful RTTs for statistics calculation
    rtts = [rtt for seq, reply, rtt in resps if reply != 'Request timed out']
    packet_loss = (1 - len(rtts) / 10) * 100  # Calculate packet loss percentage

    print("\nPing Statistics:")
    print(f"Packets: Sent = 10, Received = {len(rtts)}, Lost = {10 - len(rtts)} ({packet_loss:.1f}% loss)")

    if rtts:
        print(f"Minimum RTT: {min(rtts):.6f} seconds")
        print(f"Maximum RTT: {max(rtts):.6f} seconds")
        print(f"Average RTT: {sum(rtts) / len(rtts):.6f} seconds")

if __name__ == '__main__':
    # Ping the server on localhost at port 12000
    responses = ping('127.0.0.1', 12000)
    # Display ping statistics
    compute_statistics(responses)
