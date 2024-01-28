import colorama as cr, socket
import argparse, threading as thre
from queue import Queue

# colours 

PURPLE = cr.Fore.PURPLE
GREEN  = cr.Fore.GREEN 
RESET  = cr.Fore.LIGHTBLACK_EX

# threads number

no_threads =200
 
 # thread queue

q=Queue()

print_lock = thre.Lock()


# to get if any port is open

def is_port_open(host,port) :

    try :
        
        s= socket.socket()
        s.connect((host,port))
        #for faster scan
        s.settimeout(0.2)
    
    except:
        print(f"{PURPLE}[+] {host}:{port} is closed    {RESET}", end="\r")
    
    else :
        print(f"{GREEN}[+] {host}:{port} is open    {RESET}")
    
    finally :
        s.close()
    
#get the port number and scan that using threads
        
def scan_thread() :
    global q 
    
    while True :
        # get the port number from the queue
        worker = q.get()

        #scan the the port number 
        is_port_open(worker)

        #tells the queue that the scanning for that port is done or not 
        q.task_done()

# to get the thread initialization  method 
def main(host,ports) :
    
    global q
    
    for t in range(no_threads) :
        #for each thread, start it 

        t = thre.Thread(target= scan_thread)

        #setting the thread as daemon, so it can end itself when the main function ends
        t.daemon = True

        #starting the daemon thread
        t.start()

    for worker in ports :
        
        # for each port, put that port into the queue to start scanning
        q.put(worker)

    # wait for threads ( port scanners to finish )
    q.join()

    if __name__=="__main__" :
        # parsing some parameters
        print("hello")




    
