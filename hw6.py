"""
Where solution code to hw6 should be written.  No other files should
be modified.
"""

import socket
import io
import time
import typing
import struct
import homework6
import homework6.logging


def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """
    logger = homework6.logging.get_logger("hw6-sender")
    sock.settimeout(1.01)
    chunk_size = homework6.MAX_PACKET-6
    offsets = range(0, len(data), homework6.MAX_PACKET-6)
    num_packets = 60
    n = 1

    est_rtt = 0.51
    dev_rtt = 0.0
    ack = 0
    syn = 0
    last_syn = 0
    for i in offsets:
        syn += 1
        header = bytes(str(syn), "utf8") + b'\r'
        chunk = data[i:i+chunk_size]
        start_time = time.time()
        sock.send(header + chunk)
        logger.warning("Sending {} bytes...".format(len(header + chunk)))
        if n < num_packets and i != offsets[-1]:
            n += 1
            continue

        same_nack = -1
        init_ack = int(ack)
        is_first_timeout = True
        while int(ack) != syn:
            prev_ack = int(ack)
            try:
                ack = sock.recv(4)
            except socket.timeout:
                same_nack = -1
                logger.warning("Timeout. Asking lACK.")
                if is_first_timeout:
                    num_packets = max(prev_ack-init_ack, 10)
                    is_first_timeout = False
                sock.send(b'1')
                start_time = time.time()
                continue
            if int(ack) == prev_ack and prev_ack != same_nack:
                same_nack = prev_ack
                logger.warning("nACK: {}".format(int(ack)))
                logger.warning(" SYN: {}".format(syn))
                for k in range(prev_ack, syn):
                    offset = k*chunk_size
                    header = bytes(str(k+1), "utf8") + b'\r'
                    chunk = data[offset:offset+chunk_size]
                    sock.send(header+chunk)
                    logger.warning("2. Resending SYN: {}".format(k+1))

        finish_time = time.time()
        sample_rtt = finish_time - start_time
        est_rtt = 0.875 * est_rtt + 0.125 * sample_rtt
        dev_rtt = 0.75 * dev_rtt + 0.25 * abs(sample_rtt - est_rtt)
        sock.settimeout(est_rtt + 4 * dev_rtt)
        n = 1
        last_syn = syn

    sock.send(bytes("0", "utf8"))


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    logger = homework6.logging.get_logger("hw6-receiver")

    num_bytes = 0
    ack = 0
    is_packet_loss = True
    while True:
        data = sock.recv(homework6.MAX_PACKET)
        if not data or str(data) == "0":
            break
        if data == b'1':
            logger.warning("Resending ACK: {}".format(ack))
            sock.send(bytes(str(ack), "utf8"))
            continue
        logger.warning("Received %d bytes", len(data))
        cr_idx = -1
        for i in range(len(data)):
            if data[i:i+1] == b'\r':
                cr_idx = i
                break
        syn = int(data[:cr_idx])
        if ack != syn-1:
            if is_packet_loss:
                logger.warning("Packet loss.")
                logger.warning("lACK: {}. SYN: {}".format(ack, syn))
                sock.send(bytes(str(ack), "utf8"))
                sock.send(bytes(str(ack), "utf8"))
                sock.send(bytes(str(ack), "utf8"))
                is_packet_loss = False
            continue
        is_packet_loss = True
        ack += 1
        logger.warning("ACK: {}".format(ack))
        sock.send(bytes(str(ack), "utf8"))
        dest.write(data[cr_idx+1:])
        num_bytes += len(data)
        dest.flush()
    return num_bytes
