import random as rand
import sys

import numpy as np


class QLearner(object):

    def __init__(self, num_states=100, num_actions = 4, alpha = 0.2, gamma = 0.9,
                    rar = 0.5, radr = 0.99, dyna = 0, verbose = False):
        self.num_actions = num_actions
        self.num_states = num_states
        self.s = 0
        self.a = 0
        self.Q = np.zeros((self.num_states, self.num_actions))
        self.alpha = alpha
        self.gamma = gamma
        self.randomActionRate = rar
        self.randomActionDecay = radr
        self.dyna = dyna
        self.verbose = verbose
        self.Tc = np.full((self.num_states, self.num_actions, self.num_states), 1e-10) if dyna else None #init'd really small so that we don't get div by zero errors
        self.R = np.zeros((self.num_states, self.num_actions)) if dyna else None

    @property
    def randomActionRate(self):
        return self.__randomAction

    @randomActionRate.setter
    def randomActionRateSetter(self, val):
        if 0 <= val <= 1:
            self.__randomAction = val
        else:
            raise ValueError("Invalid RAR rate. must be between 0 and 1")

    @property
    def randomActionDecay(self):
        return self.__randomActionDecay

    @randomActionDecay.setter
    def randomActionDecaySetter(self, val):
        if 0 <= val <= 1:
            self.__randomActionDecay = val
        else:
            raise ValueError("Invalid RAR decay rate. must be between 0 and 1")

    def query(self, s):
        self.s = s
        action = self.__getNextAction(s)

        if self.verbose: print("s = {} a = {}".format(s,action))
        return action

    def training_query(self,s_prime,r):
        next_action = self.__getNextAction(s_prime, True)
        self.Q[self.s, self.a] = ((1 - self.alpha) * self.Q[self.s, self.a]) + (self.alpha * (r + (self.gamma * self.Q[s_prime, next_action])))
        if self.verbose: print("<s,a,s',r> = <{},{},{},{}> ".format(self.s, self.a, s_prime, r))
        
        # update dyna models if that's what we are doing
        if self.dyna:
            self.Tc[self.s, self.a, s_prime] += 1
            self.R[self.s, self.a] = ((1 - self.alpha) * self.R[self.s, self.a]) + (self.alpha * r)

        #save off the results before we move on to the dyna stuff
        self.s = s_prime
        self.a = next_action

        if self.dyna:
            dyna_random = np.stack([np.random.randint(0,self.num_states, self.dyna), np.random.randint(0,self.num_actions, self.dyna)], axis=1)
            for (dyna_s, dyna_a) in dyna_random:
                # time to take those shrooms
                dyna_s_prime = np.argmax(self.Tc[dyna_s, dyna_a])
                dyna_r = self.R[dyna_s, dyna_a]
                if self.verbose: print("dyna tuple = <{},{},{},{}>".format(dyna_s,dyna_a,dyna_s_prime,dyna_r))
                p1 = ((1 - self.alpha) * self.Q[dyna_s, dyna_a])
                p2 = (self.alpha * (dyna_r + (self.gamma * self.Q[dyna_s_prime, np.argmax(self.Q[dyna_s])])))
                self.Q[dyna_s, dyna_a] = (p1) + (p2)

        return self.a

    def __getNextAction(self, state, updateRAR=False):
        if rand.random() <= self.__randomAction:
            action = rand.randint(0, self.num_actions-1)
        else:
            action =  np.argmax(self.Q[state])
        if updateRAR:
            self.__randomAction *= self.__randomActionDecay
        return action

	  		 			 	 	 		 		 	  		   	  			  	
 

if __name__=="__main__":
    raise NotImplementedError("Don't call this as a stand alone program")
