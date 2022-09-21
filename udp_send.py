#!/usr/bin/env python3
import socket, argparse
from itertools import cycle
from params import (UDP_PORT, UDP_PLD_LEN, UDP_STRUCT, FILE_SIZE)
from sock_ext import setsockopt

AC0_TOS = 200
AC1_TOS = 150
AC2_TOS = 100
AC3_TOS = 50

UDP_BUFFER = b'0' * UDP_PLD_LEN
UDP_PACKET = lambda x: UDP_STRUCT.pack(x, *UDP_BUFFER)

class NumberSwitch:
    def __init__(self, N:int, M:int):
        self.setting  = { 'N': N, 'M': M }
        self.category = cycle( self.setting.keys() )
        ##
        self.indicator = next( self.category )
        self.counter   = self.setting[ self.indicator ]
        pass

    def toggle(self) -> bool:
        self.counter -= 1
        if self.counter==0:
            self.indicator = next( self.category )
            self.counter   = self.setting[ self.indicator ]
            return True
        else:
            return False
        pass

    pass

def main(target_addr:tuple, file_size:int, N:int, M:int):
    switch = NumberSwitch(N, M)
    params = {'N':AC2_TOS, 'M':AC1_TOS}
    ##
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, params[switch.indicator])
    setsockopt( sock.fileno(), params[switch.indicator] )
    ##
    for idx,_ in enumerate(range(0, file_size, UDP_PLD_LEN)):
        if switch.toggle():
            # sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, params[switch.indicator])
            ret = setsockopt( sock.fileno(), params[switch.indicator] )
            assert(ret==0)
        ##
        packet = UDP_PACKET(idx)
        sock.sendto(packet, target_addr)
    pass

if __name__=='__main__':
    parser = argparse.ArgumentParser('UDP File Sender.')
    parser.add_argument('-n', '--file-size', type=int, default=FILE_SIZE,
        help='file size in MB.')
    parser.add_argument('-c', '--ip-addr', type=str, default='',
        help='target IP Address.')
    parser.add_argument('-p', '--port', type=int, default=UDP_PORT,
        help='target port.')
    parser.add_argument('N', type=int,
        help='The interleaved number of AC2 packets.')
    parser.add_argument('M', type=int,
        help='The interleaved number of AC1 packets.')
    ##
    args = parser.parse_args()
    _addr = (args.ip_addr, args.port)
    _size = args.file_size * (1024*1024)
    try:
        main(_addr, _size, args.N, args.M)
    except Exception as e:
        raise e
    finally:
        pass
