import zmq
import time
import sys
import threading
from Elgamal2557 import *
import re
import cPickle as pickle
import zlib

def receiver_thread(arg1, stop_event):
    global receiver_key 
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

                if not receiver_key:
                    receiver_key = pickle.loads(msg)
                    print receiver_key, "receiver_key"
                    continue

                in_dict = pickle.loads(msg)
                #print in_dict,"<- in_dict"
                if 'c' in in_dict:
                    plaintext = decrypt_string(in_dict['c'], key)
                    print "receive", plaintext

                elif 'f' in in_dict:
                    print "receive file"
                    print in_dict['f']
                    frecv = BitStream(in_dict['f'])
                    sys.stdout.write(">")
                    sys.stdout.flush()
                    f = open(in_dict['fname'], "wb")
                    frecv.tofile(f)
                    f.close()

                elif 'fc' in in_dict:
                    print "receive encrypted file"
                    frecv = BitStream(decrypt(in_dict['fc'], key))
                    sys.stdout.write(">")
                    sys.stdout.flush()
                    f = open(in_dict['fname'], "wb")
                    frecv.tofile(f)
                    f.close()

                #in case of message message doesn't be encrypted
                if 'p' in in_dict:
                    plaintext = in_dict['p']
                    print "receive", plaintext 

                if 's' in in_dict:
                    if 'f' in in_dict or 'fc' in in_dict:
                        digest = AHash(int(in_dict['k']), receiver_key[0], BitStream(frecv))
                    else:
                        digest = hash_string(int(in_dict['k']), receiver_key[0], plaintext)

                    if verify(digest, in_dict['s'], receiver_key):
                        print "Verfiying Pass"

                    sys.stdout.write(">")
                    sys.stdout.flush()

if __name__ == "__main__":
    t_stop = threading.Event()
    thread = threading.Thread(target = receiver_thread, args=(1, t_stop))
    thread.start()

    receiver_key = ()

    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://161.246.5.28:%s" % port)

    #key generation
    n, k = sys.argv[1:]
    print n, k, "<- n k"
    key = gen_key(10)
    pub_key_str = pickle.dumps(key[0])
    socket.send(pub_key_str)

    while True:
        input = raw_input(">")
        message = {}

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

        if input == "":
            continue 

        if 'f' in command:
            #sending file
            try:
                file_send = BitStream(filename=input)
            except:
                print "no such file"
                continue


            if 'e' in command:
                print "sending encrypt file"
                message['fc'] =encrypt(file_send, receiver_key)
            else:
                print "sending file"
                message['f'] = file_send

            if 's' in command:
                digest = AHash(int(k), key[0][0], file_send)
                message['s'] = elgamal_sign(digest, key)
                message['k'] = k

            message['fname'] = input
            sending_str = pickle.dumps(message, -1)

        #for normal message
        else:
            if 'e' in command:
                print receiver_key , " <- receiver key"
                ciphertext = encrypt_string(input, receiver_key)
                print ciphertext, " <- cihpertext"
                message['c'] = ciphertext

            #don't encrypt
            else:
                message['p'] = input

            if 's' in command:
                digest = hash_string(int(k), key[0][0], input)
                signature = elgamal_sign(digest, key)
                message['s'] = signature
                message['k'] = k

            print message,  "message"

            sending_str = pickle.dumps(message)

        socket.send(sending_str)

        time.sleep(1)
