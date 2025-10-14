



import threading
import time
from utils.logger import setup_logger
import json
from fsm import FSM


STATE_FILE = "data/shared_state.json"
# to do 
# step 1  :-make three function like idel wait and move hadler 
class Lift(FSM):
    def __init__(self, total_floors: int):
        self.idele="IDELE"
        self.moving_up="MOVING-UP"
        self.sleeping="SLEEPING"
        self.moving_down="MOVING-DOWN"
        self.waiting="WAITING"
        self.state=""


        self.current_floor = 0
        self.total_floors = total_floors
        self.list_floor = {}
        self.lock = threading.Lock()
        self.logger= setup_logger("lift")
 
      
        super().__init__(name="liftFSM", robot_obj=self, logger=self.logger)

        self.add_state("IDLE", "IDLE", lambda: self.idle_state())
        self.add_state("MOVING_UP", "MOVING_UP", lambda: self.moving_up_state())
        self.add_state("MOVING_DOWN", "MOVING_DOWN", lambda: self.moving_down_state())
        self.add_state("WAITING", "WAITING", lambda: self.waiting_state())
        self.add_state("SLEEPING", "SLEEPING", lambda: self.sleep_state())
        self.set_current_state("IDLE")
        self.start_fsm_thread()
      
 

        
    def idle_state(self):
        self.state = self.idele
        self.logger.info(f"State: IDLE | Current floor: {self.current_floor}")
        if self.list_floor:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return "MOVING_UP"
            elif next_floor < self.current_floor:
                return "MOVING_DOWN"
        self.sleep_fsm() 
        return "SLEEPING"
    
    

    def sleep_state(self):
        self.state = self.sleeping
        self.logger.info(f"State: SLEEPING | Current floor: {self.current_floor}")
        self.sleep_fsm() 
        return "SLEEPING"

    def moving_up_state(self):
        # lift = fsm.robot_obj
        self.state = self.moving_up
        self.logger.info(f"Moving up from floor {self.current_floor}")
        dict(sorted(self.list_floor.items()))
        
        self.current_floor += 1
        time.sleep(2)
        
        if (
            self.current_floor in self.list_floor and 
            (
            
                self.list_floor[self.current_floor] in ("up", None)
             
                or self.current_floor in (0, self.total_floors)
            )
        ):     
            self.logger.info(f"Reached floor ===========================================>{self.current_floor}")
            self.list_floor.pop(self.current_floor, None)
            return "WAITING"

        if not self.list_floor:
            return "IDLE"

        next_floor = next(iter(self.list_floor))
        return "MOVING_UP" if next_floor > self.current_floor else "MOVING_DOWN"


    def moving_down_state(self): 
        # lift = fsm.robot_obj
        self.state = self.moving_down
        dict(sorted(self.list_floor.items(), reverse=True))
        self.logger.info(f"Moving down from floor {self.current_floor}")

        self.current_floor -= 1
        time.sleep(2)
        if (
            self.current_floor in self.list_floor and 
            (
            
                self.list_floor[self.current_floor] in ("down", None)
             
                or self.current_floor in (0, self.total_floors)
            )
        ):     

            self.logger.info(f"Reached floor ===========================================>{self.current_floor}")
            self.list_floor.pop(self.current_floor, None)
            return "WAITING"

        if not self.list_floor:
            return "IDLE"

        next_floor = next(iter(self.list_floor))
        return "MOVING_DOWN" if next_floor < self.current_floor else "MOVING_UP"


    
    def waiting_state(self):
        self.state = self.waiting
        self.logger.info(f"Waiting at floor {self.current_floor}")
        time.sleep(2)
        if self.list_floor:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return "MOVING_UP"
            elif next_floor < self.current_floor:
                return "MOVING_DOWN"
        return "IDLE"
    

    
 



