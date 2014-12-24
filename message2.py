import zmq
import time
import sys
import threading
import cPickle as pickle
import zlib
from Elgamal2557 import *

def send_zipped_pickle(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return socket.send(z, flags=flags)

def decomp_zipped_pickle(msg_recv):
    """inverse of send_zipped_pickle"""
    z = msg_recv
    p = zlib.decompress(z)
    return pickle.loads(p)


def receiver_thread(arg1, stop_event):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    ffflag, fflag = False, False

    while(not stop_event.is_set()):
        socks = dict(poller.poll(1000))
        if socks:
            if socks.get(socket) == zmq.POLLIN:
                msg = socket.recv(zmq.NOBLOCK)

                if msg == "!file":
                    print "inside checksend"
                    fflag = True
                else:
                    fflag = False

                if ffflag == False:
                    print "receive: ", msg
                    sys.stdout.write(">")
                    sys.stdout.flush()
                    if fflag == True:
                        ffflag = True
                else:
                    #print "raw message to loads:", msg
                    #dsmsg = decomp_zipped_pickle(msg)
                    dsmsg = pickle.loads(msg)
                    #print dsmsg
                    sys.stdout.write(">")
                    sys.stdout.flush()
                    frecv = BitStream(dsmsg)
                    f = open("file.out", "wb")
                    frecv.tofile(f)
                    f.close()
                    msg = "cleared"
                    fflag = False
                    ffflag = False

if __name__ == "__main__":
    t_stop = threading.Event()
    thread = threading.Thread(target = receiver_thread, args=(1, t_stop))
    thread.start()


    port = "5557"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:%s" % port)

    while True:
        input = raw_input(">")

        if input == "stop":
            t_stop.set()
            print "exit program"
            sys.exit()
        socket.send(input)
        time.sleep(1)
