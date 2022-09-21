#!/usr/bin/env python3
import socket, time, struct
import argparse
from math import ceil
from params import (UDP_PLD_LEN, UDP_PORT, FILE_SIZE)

def main(port:int, number:int, ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))

    received = 0
    packet_list = [-1] * number
    time_start, time_stop = 0, 0

    while True:
        try:
            data, _ = sock.recvfrom(1500)
            if time_start==0:
                time_start = time.time()
            ##
            # data = UDP_STRUCT.unpack(data)
            idx  = struct.unpack('I', data[:4])
            packet_list[ received ] = idx
            received += 1
            ##
            if received==number:
                time_stop = time.time()
                break
        except Exception as e:
            raise e
        pass

    print('Elapsed: ', time_stop - time_start)

if __name__=='__main__':
    parser = argparse.ArgumentParser('UDP File Receiver.')
    parser.add_argument('-n', '--file-size', type=int, default=FILE_SIZE,
        help='file size in MB.')
    parser.add_argument('-p', '--port', type=int, default=UDP_PORT,
        help='target port.')
    ##
    args = parser.parse_args()
    _file_size = args.file_size * (1024*1024)
    number = ceil( _file_size / UDP_PLD_LEN )
    try:
        main(args.port, number)
    except Exception as e:
        raise e
    finally:
        pass
