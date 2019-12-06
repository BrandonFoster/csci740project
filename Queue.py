import numpy as np
import math

class Queue:

    ''' 
    next_person -> A fuction that will give the time to the next person when called
    service_time -> A fuction that will give a service time when called
    servers -> the number of servers in the simulation
    '''
    def __init__(self, next_person, service_time, servers):
        self.service_time = service_time
        self.clocks = [0]
        self.servers = []
        self.clocks[0] = self.next_person()
        self.next_times = [self.next_person]
        for i in range(servers):
            self.servers.append(Server(service_time))
            self.clocks.append(self.service_time())
            self.next_times.append(self.service_time)
        self.queue = [] #Kibum
        
    def get_queue(self):
        return self.queue

    '''
    Returns the index of the next free server
    Returns -1 if no servers are avalible
    '''
    def free_servers(self):
        i = -1
        try:
            i = self.servers.index(False)
        except ValueError:
            i = -1
        return i
    '''
    server -> index of the server
    simulates a server taking a customer
    '''
    def take_customer(self,server):
        self.servers[server] = True

    '''
    server -> index of the server
    ends the service of a server
    '''
    def end_service(self, server):
        if len(self.queue) > 0:
            self.queue.pop(0)   #Kibum
        else:
            self.servers[server] = False
    '''
    time -> the amount of time the simulation has advanced
    updates all of the clocks
    '''
    def update_clocks(self,time):
        #subtract the time and then regerate the time that ran out
        for c in range(len(self.clocks)):
            self.clocks[c] -= time
            if self.clocks[c] == 0:
                self.clocks[c] = self.next_times[c]()
                
    def simulate(self, total_time):
        # start the simulation at time 0
        time = 0
        # Main simuation looop
        while True:
            #find the next event and time untill the next event
            event_time = min(self.clocks)
            event = self.clocks.index(event_time)
            time += event_time
            print(self.clocks)
            # run the simulation untill the time is past the total time
            if time > total_time:
                break
            #The event of someone arriving
            if event == 0:
                # If the queue has peaple in it just add to the queue
                if len(self.queue) > 0: #Kibum
                    self.queue.append(1)    #Kibum
                else:
                    # if there is a free server send the customer to that server
                    server = self.free_servers()
                    if server > -1:
                        self.take_customer(server)
                    # If there are no free servers then put the customer in the queue
                    else:
                        self.queue.append(1)    #Kibum
            # A server has finished
            else:
                self.end_service(event - 1)
            #update the clock
            self.update_clocks(event_time)
            
def problem2_arrivals():
    return np.random.exponential(1)
def problem2_service():
    return np.random.gamma(3,0.25)

q = Queue(problem2_arrivals, problem2_service, 4)
