import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

class TradingQAgent:
    def __init__(self, env):
        self.env = env
        self.lr = 0.1 
        self.gamma = 0.95
        self.eps = 0.5
        self.decay = 0.99995
        self.q_table = pd.DataFrame(columns=list(range(env.action_space.n)), 
                                    dtype=np.float64)
                                    
    def train(self, episodes):
        for e in range(episodes):
            state = self.env.reset()
            done = False
            score = 0
            
            while not done:
                action = self.get_action(state)
                next_state, reward, done, _ = self.env.step(action)

                self.update_qtable(state, action, reward, next_state)
                
                state = next_state
                score += reward
                
            self.eps = max(0.01, self.eps*self.decay)        
            print("Episode {} Score {}".format(e,score))
            
            
    def get_action(self, state):
        #print("current espilon" , self.eps)
        if np.random.random() < self.eps:
            return self.env.action_space.sample()
        else:
            try :
                cho_action =  np.argmax(self.q_table[self.q_table.index == tuple(state)].values)    
                if cho_action!= 0 : print("chosen action", cho_action)
                return cho_action
            except Exception as e :
                print(e)
                #cho_action =  self.env.action_space.sample()
            
            
            
    def update_qtable(self, state, action, reward, next_state):
        #print("state", state)
        #print("action", action)
        #print("next_state", next_state)
        #print(self.q_table.values)
        tup_state = tuple(state)
        tup_next_state = tuple(next_state)
        if tup_state not in self.q_table.index :
            #print("state not in table")
            #print("before", self.q_table)
            self.q_table = self.q_table.append(
            pd.Series([0]*3, index=self.q_table.columns, name=tup_state))
            #print("index" ,self.q_table.index)
            #print('tup', pd.Index(tup_state, dtype="object"))
            #print("after", self.q_table)
        try :
            current_value = self.q_table[self.q_table.index == tup_state][action]
        except :
            current_value = 0
        if tup_next_state not in self.q_table.index :
            #print("next_state not in table")
            #print("before", self.q_table)
            self.q_table = self.q_table.append(
            pd.Series([0]*3, index=self.q_table.columns, name=tup_next_state))
            #print("after", self.q_table)
        
        max_next_value = np.max(self.q_table[self.q_table.index == tup_next_state].values)

        new_value = (1 - self.lr) * current_value + \
                   self.lr * (reward + self.gamma * max_next_value)
        
        try :
            self.q_table[action] = np.where(self.q_table.index == tup_state, new_value, self.q_table[action])
        except :
            pass
        
        """q_1 = self.q_table.loc[tuple(state)][action]
        q_2 = reward + self.gamma*max(self.q_table.loc[tuple(next_state)])
        self.q_table.loc[tuple(state)][action] += self.lr*(q_2 - q_1)  
        """
        
        
    def test(self, episodes):
        for e in range(episodes):
            done = False
            score = 0
            state = self.env.reset()
            
            while not done:
                if tuple(state) in self.q_table.index :
                    action = np.argmax(self.q_table[self.q_table.index == tuple(state)].values)#np.argmax(self.q_table.loc[tuple(state)])
                    state, reward, done, _ = self.env.step(action)
                    
                    score += reward
                    
            print("Test {} Score {}".format(e, score))
  