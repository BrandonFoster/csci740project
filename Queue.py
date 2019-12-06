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
    red        -> [0,1] likeliness of the customer enjoying red
    white      -> [0,1] likeliness of the customer enjoying white
    sweat      -> [0,1] likeliness of the customer enjoying sweat
    dry        -> [0,1] likeliness of the customer enjoying dry
    money      -> money in dollar bills that the customer is willing to spend on wine
    taste_time -> amount of time to taste the wine in minutes
    Returns a dictionary of bottles bought where the key is the name of the wine
    the value is the amount purchased
    '''
    def wine_tasting(self, red, white, sweet, dry, money, taste_time):
        #price for wine bottle in dollars
        price_sweet_red   = 14
        price_sweet_white = 12
        price_dry_red     = 25
        price_dry_white   = 20
         
        #types of wine combinations
        sweet_red   = sweet*red
        sweet_white = sweet*white
        dry_red     = dry*red
        dry_white   = dry*white

        #grabs the total of the combinations
        tot_wine_comb = sweet_red + sweet_white + dry_red + dry_white
        
        #calculates the amount of wine bought based on each combination
        taste = taste_time/10 #time tasting the wine as a ratio over an average time of 10 minutes

        #potential bottles of wine to buy for each
        pot_sweet_red   = math.floor(taste*(sweet_red/tot_wine_comb)*(money/price_sweet_red))
        pot_sweet_white = math.floor(taste*(sweet_white/tot_wine_comb)*(money/price_sweet_white))
        pot_dry_red     = math.floor(taste*(dry_red/tot_wine_comb)*(money/price_dry_red))
        pot_dry_white   = math.floor(taste*(dry_white/tot_wine_comb)*(money/price_dry_white))

        #buys bottles from the most to least enjoyed
        bottle_dict = {"sweet red":0, "sweet white":0, "dry red":0, "dry white":0}
        comb_dict = {"sweet red":sweet_red, "sweet white":sweet_white, "dry red":dry_red, "dry white":dry_white}
        enjoyed_list = [sweet_red, sweet_white, dry_red, dry_white]
        enjoyed_list.sort()
        enjoyed_list.reverse()
        for value in enjoyed_list:
            comb = self.match_comb(comb_dict, value)
            if("sweet red" == comb):
                max_sweet_red = math.floor(money/price_sweet_red)
                bought = min(max_sweet_red, pot_sweet_red)
                money -= bought*price_sweet_red
                bottle_dict["sweet red"] = bought
            if("sweet white" == comb):
                max_sweet_white = math.floor(money/price_sweet_white)
                bought = min(max_sweet_white, pot_sweet_white)
                money -= bought*price_sweet_white
                bottle_dict["sweet white"] = bought
            if("dry red" == comb):
                max_dry_red = math.floor(money/price_dry_red)
                bought = min(max_dry_red, pot_dry_red)
                money -= bought*price_dry_red
                bottle_dict["dry red"] = bought
            if("dry white" == comb):
                max_dry_white = math.floor(money/price_dry_white)
                bought = min(max_dry_white, pot_dry_white)
                money -= bought*price_dry_white
                bottle_dict["dry white"] = bought
            comb_dict.pop(comb, None)

        return bottle_dict

    '''
    Used with the wine_tasting() function
    '''
    def match_comb(self, comb_dict, value):
        for comb in comb_dict:
            if(comb_dict[comb] == value):
                return comb
    
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
