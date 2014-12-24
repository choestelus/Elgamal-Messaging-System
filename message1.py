import zmq
import time
import sys
import threading
import cPickle as pickle
import zlib
import json
from Elgamal2557 import *

def send_zipped_pickle(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    print "obj=", obj
    p = pickle.dumps(obj, protocol)
    #z = zlib.compress(p)
    return socket.send(p, flags=flags)

def recv_zipped_pickle(socket, flags=0, protocol=-1):
    """inverse of send_zipped_pickle"""
    z = socket.recv(flags)
    p = zlib.uncompress(z)
    return pickle.loads(p)

def receiver_thread(arg1, stop_event):
    port = "5557"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    while(not stop_event.is_set()):
        socks = dict(poller.poll(1000))
        if socks:
            if socks.get(socket) == zmq.POLLIN:
                msg = socket.recv(zmq.NOBLOCK)
                print "receive: ", msg
                sys.stdout.write(">")
                sys.stdout.flush()

if __name__ == "__main__":
    t_stop = threading.Event()
    thread = threading.Thread(target = receiver_thread, args=(1, t_stop))
    thread.start()

    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:%s" % port)

    key = gen_key(32)
    file_send = BitStream(filename="README.md")
    flag_sndfile = False
    while True:
        input = raw_input(">")
        if input == "stop":
            t_stop.set()
            print "exit program"
            sys.exit()
        elif input == "!file":
            flag_sndfile = True
            print "sending file"
            socket.send("!file")
            time.sleep(1)
            send_zipped_pickle(socket, file_send)

        if flag_sndfile == False:
            socket.send(input)
        flag_sndfile = False
        time.sleep(1)
