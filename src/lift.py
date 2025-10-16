



import threading
import time
from utils.logger import setup_logger
import json
from fsm import FSM
import utils.settings as settings


STATE_FILE = "data/shared_state.json"
# to do 
# step 1  :-make three function like idel wait and move hadler 
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
        self.logger= setup_logger("lift")
        print("lift class is here ")
        print("lift list of floor "+str(self.list_floor))
      
        super().__init__(name="liftFSM", robot_obj=self, logger=self.logger)

        self.add_state("IDLE", "IDLE", lambda: self.idle_state())
        self.add_state("MOVING-UP", "MOVING-UP", lambda: self.moving_up_state())
        self.add_state("MOVING-DOWN", "MOVING-DOWN", lambda: self.moving_down_state())
        self.add_state("WAITING", "WAITING", lambda: self.waiting_state())

        self.add_state("EMERGENCY", "EMERGENCY", lambda: self.emergency_state())
        self.add_state("RESUME", "RESUME", lambda: self.resume_state())
        self.set_current_state("IDLE")
        self.start_fsm_thread()
      
 
    def emergency_state(self): 
        self.logger.warning(f"State--> emergency stop at current floor: {self.current_floor}")
        return "WAITING"
    
     
    
    def resume_state(self):
        settings.FLAG_EMERGANCY=False
        self.logger.info(f"State-->resume returning to ground from {self.current_floor}")
        return "MOVING-DOWN"
         
    
    def idle_state(self):
    
        self.logger.info(f"State: IDLE  current floor: {self.current_floor}")
        if settings.FLAG_EMERGANCY==True:
            return "EMERGENCY"
        if len(self.list_floor)>0:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return "MOVING-UP"
            elif next_floor < self.current_floor:
                return "MOVING-DOWN"
        else:
            self.logger.info(f"State: IDLE (sleep)  Current floor: {self.current_floor}")
            self.sleep_fsm() 
          
       
    


    def moving_up_state(self):
        self.logger.info(f"Moving up from floor {self.current_floor}")
        if settings.FLAG_EMERGANCY==True:
            self.current_floor = min(self.current_floor + 1,self.total_floors)
            return "EMERGENCY"
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
                    return "WAITING"
        if not self.list_floor:
            return "IDLE"

       


    def moving_down_state(self): 
       
        if settings.FLAG_EMERGANCY==True:
            self.current_floor = max(self.current_floor - 1,0)
            return "EMERGENCY"
        if settings.FLAG_RESUME == True:

            
            
            if self.current_floor != 0:
                self.current_floor -= 1
                time.sleep(2)
                self.logger.info(f"Lift moving down during resume. Now at floor {self.current_floor}")
            else:
                self.logger.info("Lift reached at ground floor.")

                settings.FLAG_RESUME = False
                return "IDLE"
            
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
                if (
                    self.current_floor in self.list_floor 
                    # (
                    
                    #     value in ("DOWN", None)
                    
                    #     or self.current_floor in (0, self.total_floors)
                    # )
                ):     
                    if  len(self.list_floor) == 1 or direction in ("DOWN", None) or self.current_floor in (0, self.total_floors):
                   
                        self.logger.info(f"Reached at floor ==================>{self.current_floor}")
            
                        self.list_floor.pop(self.current_floor)
                        return "WAITING"
        
          
            else:
                return "IDLE"
        
        


    
    def waiting_state(self):
        if settings.FLAG_EMERGANCY == True:
            self.logger.info("Waiting for user input to resume at floor{}".format(str(self.current_floor)))
            self.sleep_fsm() 
            
        if settings.FLAG_RESUME ==True:
            return "RESUME"

        
        else:
            self.logger.info(f"Waiting at floor {self.current_floor}")
            time.sleep(2)
            # if self.list_floor:
            #     next_floor = next(iter(self.list_floor))
            #     if next_floor > self.current_floor:
            #         return "MOVING-UP"
            #     elif next_floor < self.current_floor:
            #         return "MOVING-DOWN"
            return "IDLE"
    

    
 



