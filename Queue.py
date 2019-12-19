import numpy as np
import math
from Customer import Customer
from Server import Server

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
        self.clocks[0] = next_person()
        self.next_times = [next_person]
        for i in range(servers):
            self.servers.append(Server(service_time))
            self.clocks.append(self.service_time())
            self.next_times.append(self.service_time)
        self.queue = []
        self.sales = {"sweet red":0, "dry red":0, "sweet white":0, "dry white": 0}
        self.sweet_red = 14
        self.sweet_white = 12
        self.dry_red = 25
        self.dry_white = 20
        self.tasting_profits = 0
        
    def get_queue(self):
        return self.queue

    '''
    Returns the index of the next free server
    Returns -1 if no servers are avalible
    '''
    def free_servers(self):
        for s in range(len(self.servers)):
            if self.servers[s].customer is None:
                return s
        return -1
    '''
    server -> index of the server
    simulates a server taking a customer
    '''
    def take_customer(self,server, customer):
        self.servers[server].customer = customer
        self.servers[server].time = self.clocks[server + 1]
        self.tasting_profit += 5

    '''
    server -> index of the server
    ends the service of a server
    '''
    def end_service(self, server):
        self.sell_wine(self.servers[server].customer)
        if len(self.queue) > 0:
            self.take_customer(server,self.queue.pop(0))
        else:
            self.servers[server].customer = None

    def sell_wine(self, customer):
        wine_sold = self.wine_tasting(customer)
        for wine in wine_sold:
            self.sales[wine] += wine_sold[wine]
    '''
    Returns a dictionary of bottles bought where the key is the name of the wine
    the value is the amount purchased
    '''
    def wine_tasting(self, customer):

        sweet = customer.affinity[0]
        dry = customer.affinity[1]
        white = customer.affinity[2]
        red = customer.affinity[3]
        money = np.random.uniform()*customer.max_budget
        taste_time = customer.time
        
        #price for wine bottle in dollars
        price_sweet_red   = self.sweet_red
        price_sweet_white = self.sweet_white
        price_dry_red     = self.dry_red
        price_dry_white   = self.dry_white
         
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
        for s in self.servers:
            if not(s.customer is None):
                s.customer.time += time
                
    def simulate(self, total_time):
        # start the simulation at time 0
        time = 0
        self.tasting_profit = 0
        for i in self.sales:
            self.sales[i] = 0
        # Main simuation looop
        while True:
            #find the next event and time untill the next event
            event_time = min(self.clocks)
            event = self.clocks.index(event_time)
            time += event_time
            # update the clock
            self.update_clocks(event_time)
            # run the simulation untill the time is past the total time
            if time > total_time:
                break
            #The event of someone arriving
            if event == 0:
                # If the queue has peaple in it just add to the queue
                if len(self.queue) > 0:
                    self.queue.append(Customer())
                else:
                    # if there is a free server send the customer to that server
                    server = self.free_servers()
                    if server > -1:
                        self.take_customer(server,Customer())
                    # If there are no free servers then put the customer in the queue
                    else:
                        self.queue.append(Customer())
            # A server has finished
            else:
                self.end_service(event - 1)
        return self.total_profit()

    def total_profit(self):
        dred_prof = self.sales["dry red"] * self.dry_red
        dwhite_prof = self.sales["dry white"] * self.dry_white
        sred_prof = self.sales["sweet red"] * self.sweet_red
        swhite_prof = self.sales["sweet white"] * self.sweet_white
        return dred_prof + dwhite_prof + sred_prof + swhite_prof + self.tasting_profit
    def mass_simulate(self, iterations):
        total = 0
        for i in range(iterations):
            total += self.simulate(480)
        return total/iterations
            
def problem2_arrivals():
    return np.random.exponential(0.20)
def problem2_service():
    return np.random.gamma(5,2)

q = Queue(problem2_arrivals, problem2_service, 4)
