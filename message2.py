import zmq
import time
import sys
import threading

def receiver_thread(arg1, stop_event):
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
                print "receive: ", msg ,"\n>"
                socket.send("Server've received message")

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
