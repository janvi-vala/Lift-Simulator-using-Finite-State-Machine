



import threading
import time
from utils.logger import setup_logger
import json

logger = setup_logger("lift")
STATE_FILE = "data/shared_state.json"
# to do 
# step 1  :-make three function like idel wait and move hadler 
class Lift:
    def __init__(self, total_floors: int):
        self.idele="IDELE"
        self.moving_up="MOVING-UP"
        self.moving_down="MOVING-DOWN"
        self.waiting="WAITING"
        self.current_floor = 0
        self.total_floors = total_floors
        self.list_floor = {}
        self.lock = threading.Lock()
        self.running = True
        self.update_state("while_condition", True)
       
        self.flag_moving = False
        self.state=""
        self.thread = threading.Thread(target=self.move, daemon=True)
        self.thread.start()
        
 

    def update_state(self,key, value):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
        except FileNotFoundError:
            print("State file not found.")
        state[key] = value
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        
    def read_state(self):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("State file not found.")



    def idel_handler():
        pass 
    def wait_handler():
        pass 
    def move_handler():
        pass 
    



    def inside_lift(self,step,direction,floor=None):
        
        if (step == 1 and direction == "up") or (step == -1 and direction == "down"):
           
            self.state=self.waiting
            time.sleep(3)
            self.update_state("flag_inside_lift",True)
            state=self.read_state()
           
            
            logger.info(f"current floor :- {floor} and lift state :- {self.waiting}")
            
            
            
            if floor:
                self.list_floor.pop(floor,None)
            # self.update_state("flag_inside_lift",False)

          


    def add_request(self, floor, direction=None):
        with self.lock:
            if 0 <= floor <= self.total_floors:
               
                if floor not in self.list_floor:
                    self.list_floor[floor] = direction
               
            else:
                logger.error(f"Lift-{self.lift_id}: Invalid floor {floor}")
    def move(self):
        while self.running:

            data=self.read_state()
           
            if data.get("floor",0) != 0:
                self.add_request(data.get("floor",0))
                self.update_state("floor",0)   
            with self.lock:
                
                if  len(self.list_floor)==0:
                    if(self.state != self.idele):
                      logger.info(f"current floor :- {self.current_floor} and lift state :- {self.idele}")
                      self.state=self.idele
                    
                    time.sleep(1)
                    continue
              
                next_floor, direction = next(iter(self.list_floor.items()))

                self.list_floor.pop(next_floor)

            step = 1 if next_floor > self.current_floor else -1

            if step == 1:
               self.list_floor = dict(sorted(self.list_floor.items()))
            else:
                self.list_floor = dict(sorted(self.list_floor.items(), reverse=True))

            
            
            if next_floor== -1:
                self.running=False
                self.update_state("while_condition",False)
                
            if step==1:
                    self.state=self.moving_up
                    logger.info(f" ======>lift state :- {self.moving_up}")
            else:
                    self.state=self.moving_down
                    logger.info(f"========> lift state :- {self.moving_down}")

           
            while self.current_floor != next_floor:
                logger.info(f"current floor :- {self.current_floor} ")

                

                self.current_floor += step

                

                if self.current_floor in self.list_floor:
                        direction2=self.list_floor[self.current_floor]
                       
                        if direction2 :
                            logger.debug(f"direction{direction2}")
                            self.inside_lift(step,direction2,self.current_floor)
                        else:
                            self.state=self.waiting
                            logger.info(f"Reached floor {self.current_floor}")
                            self.list_floor.pop(self.current_floor)
                time.sleep(3)
            logger.debug(f"direction{direction} and  {next_floor}")
            if direction :
                self.inside_lift(step,direction,next_floor)
            logger.info(f": Reached floor {self.current_floor}")

    def return_to_ground_floor(self):
        self.add_request(0)



