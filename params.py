#!/usr/bin/env python
import struct

UDP_PORT = 11112
FILE_SIZE = 100#MB

UDP_MAX_LEN = 1472 #(1500-20-8)
UDP_SEQ_LEN = 4
UDP_PLD_LEN = UDP_MAX_LEN - UDP_SEQ_LEN

UDP_STRUCT = struct.Struct( 'I%dB'%(UDP_PLD_LEN) )
