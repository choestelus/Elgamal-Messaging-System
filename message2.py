import zmq
import time
import sys
import threading
from Elgamal2557 import *
import re
import pickle

def receiver_thread(arg1, stop_event):
    global receiver_key 
    port = "5556"
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

                if not receiver_key:
                    receiver_key = pickle.loads(msg)
                    print receiver_key, "receiver_key"
                    continue

                print "receive: ",
                print decrypt_string(pickle.loads(msg), key)
                sys.stdout.write(">")
                sys.stdout.flush()


if __name__ == "__main__":
    t_stop = threading.Event()
    thread = threading.Thread(target = receiver_thread, args=(1, t_stop))
    thread.start()

    receiver_key = ()

    port = "5557"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://localhost:%s" % port)

    #key generation
    n, k = sys.argv[1:]
    print n, k, "<- n k"
    key = gen_key(10)
    pub_key_str = pickle.dumps(key[0])
    socket.send(pub_key_str)

    while True:
        input = raw_input(">")

        try:
            command = re.search('^\$.*\s', input).group(0)[:-1]
            input = input.split(" ", 1)[1]
        except AttributeError:
            command = ""

        if input == "$q":
            t_stop.set()
            print "exit program"
            socket.close()
            sys.exit()
            print "after exit"

        if input == "":
            continue 

        if 'f' in command:
            #sending file
            pass

        if 'e' in command:
            print receiver_key , " <- receiver key"
            ciphertext = encrypt_string(input, receiver_key)
            print ciphertext, " <- cihpertext"
            sending_str = pickle.dumps(ciphertext)
            
        socket.send(sending_str)
        time.sleep(1)
