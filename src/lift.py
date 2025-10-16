
import threading
import time
from utils.logger import setup_logger
from fsm import FSM



class Lift(FSM):
    def __init__(self, total_floors: int):

        self.state={
            0:"IDLE",
            1:"MOVING-UP",
            2:"MOVING-DOWN",
            3:"WAITING",
            4:"EMERGENCY",
            5:"RESUME",
        
        }

        self.flag_resume=False
        self.current_floor = 0
        self.total_floors = total_floors
        self.list_floor = {}
        self.lock = threading.Lock()
        self.FLAG_EMERGANCY=False
        self.FLAG_RESUME=False
        self.logger= setup_logger("lift")
        print("lift class is here ")
        print("lift list of floor "+str(self.list_floor))
      
        super().__init__(name="liftFSM", robot_obj=self, logger=self.logger)

        self.add_state(self.state[0], self.state[0], lambda: self.idle_state())
        self.add_state(self.state[1], self.state[1], lambda: self.moving_up_state())
        self.add_state(self.state[2], self.state[2], lambda: self.moving_down_state())
        self.add_state(self.state[3], self.state[3], lambda: self.waiting_state())

        self.add_state(self.state[4], self.state[4], lambda: self.emergency_state())
        self.add_state(self.state[5], self.state[5], lambda: self.resume_state())
        self.set_current_state(self.state[0])
        self.start_fsm_thread()
      
 
    def emergency_state(self): 
        self.logger.warning(f"State--> emergency stop at current floor: {self.current_floor}")
        return self.state[3]
    
     
    
    def resume_state(self):
        self.FLAG_EMERGANCY=False
        self.logger.info(f"State-->resume returning to ground from {self.current_floor}")
        return self.state[2]
         
    
    def idle_state(self):
    
        self.logger.info(f"State: IDLE  current floor: {self.current_floor}")
        if self.FLAG_EMERGANCY==True:
            return self.state[4]
        if len(self.list_floor)>0:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return self.state[1]
            elif next_floor < self.current_floor:
                return self.state[2]
        else:
            self.logger.info(f"State: IDLE (sleep)  Current floor: {self.current_floor}")
            self.sleep_fsm() 
          
       
    


    def moving_up_state(self):
        self.logger.info(f"Moving up from floor {self.current_floor}")
        if self.FLAG_EMERGANCY==True:
            self.current_floor = min(self.current_floor + 1,self.total_floors)
            return self.state[4]
        up_floors = sorted(
                f for f in self.list_floor.keys()
                if isinstance(f, int) and f > self.current_floor
            )
      
        if up_floors:    
            self.current_floor += 1
            time.sleep(2)
            direction = self.list_floor.get(self.current_floor,None)
            if (self.current_floor in self.list_floor):     
               if  len(self.list_floor) == 1 or direction in ("UP", None) or self.current_floor in (0, self.total_floors):
                    self.logger.info(f"Reached floor ===========================================>{self.current_floor}")
                    self.list_floor.pop(self.current_floor)
                    return self.state[3]
        if not self.list_floor:
            return self.state[0]

       


    def moving_down_state(self): 
       
        if self.FLAG_EMERGANCY==True:
            self.current_floor = max(self.current_floor - 1,0)
            return self.state[4]
        if self.FLAG_RESUME == True:

            
            
            if self.current_floor != 0:
                self.current_floor -= 1
                time.sleep(2)
                self.logger.info(f"Lift moving down during resume. Now at floor {self.current_floor}")
            else:
                self.logger.info("Lift reached at ground floor.")

                self.FLAG_RESUME = False
                return self.state[0]
            
        else:
            self.logger.info(f"Moving down from floor {self.current_floor}")
            down_floors = sorted(
            (f for f in self.list_floor.keys() 
            if isinstance(f, int) and f < self.current_floor ),
            reverse=True
        )
            if down_floors:
                self.current_floor -= 1
                time.sleep(2)
                direction= self.list_floor.get(self.current_floor,None)
                if ( self.current_floor in self.list_floor  ):     
                    if  len(self.list_floor) == 1 or direction in ("DOWN", None) or self.current_floor in (0, self.total_floors):
                   
                        self.logger.info(f"Reached at floor ==================>{self.current_floor}")
            
                        self.list_floor.pop(self.current_floor)
                        return self.state[3]
        
          
            else:
                return self.state[0]
        
        


    
    def waiting_state(self):
        if self.FLAG_EMERGANCY == True:
            self.logger.info("Waiting for user input to resume at floor{}".format(str(self.current_floor)))
            self.sleep_fsm() 
            
        if self.FLAG_RESUME ==True:
            return self.state[5]

        
        else:
            self.logger.info(f"Waiting at floor {self.current_floor}")
            time.sleep(2)
            return self.state[0]
    

    
 



