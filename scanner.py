import colorama as cr, socket
import argparse, threading as thre
from queue import Queue

# colours 
cr.init()
YELLOW = cr.Fore.YELLOW
GREEN  = cr.Fore.GREEN 
RESET  = cr.Fore.RESET

# threads number

no_threads =200
 
 # thread queue

q=Queue()

print_lock = thre.Lock()


# to get if any port is open

def is_port_open(port) :

    try :
        
        s= socket.socket()
        s.connect((host,port))
        #for faster scan
        #s.settimeout(0.2)
    
    except:
        with print_lock :
            print(f"{YELLOW}[+] {host}:{port} is closed    {RESET}", end="\r")
    
    else :
        with print_lock :
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
        
        parser = argparse.ArgumentParser(description="Simple port scanner")
        parser.add_argument("host", help ="host to scan ")
        parser.add_argument("--ports","-p",dest= "port_range", default = "1-65535",help="port range to scan, default is 1 to 65535")
        args = parser.parse_args()
        host,port_range= args.host, args.port_range

        start_port, end_port = port_range.split("-")
        start_port, end_port =int(start_port),int(end_port)
        
        ports= [p for p in range(start_port,end_port)]

        main(host,ports)




    
