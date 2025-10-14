



import threading
import time
from utils.logger import setup_logger
import json


STATE_FILE = "data/shared_state.json"
# to do 
# step 1  :-make three function like idel wait and move hadler 
class Lift:
    def __init__(self, total_floors: int):
        self.idele="IDELE"
        self.moving_up="MOVING-UP"
        self.sleeping="SLEEPING"
        self.moving_down="MOVING-DOWN"
        self.waiting="WAITING"
        self.current_floor = 0
        self.total_floors = total_floors
        self.list_floor = {}
        self.lock = threading.Lock()
        self.logger= setup_logger("lift")
 
        self.state=""
      
    print("inside the left class")
    def add_request(self, floor, direction=None,fsm=None):
       
        with self.lock:
            if 0 <= floor <= self.total_floors:
                
                if floor not in self.list_floor:
                    self.list_floor[floor] = direction
                if self.state==self.sleeping:
                    fsm.wake_up()
                
            else:
                self.logger.error(f"Lift Invalid floor {floor}")

        

    def idle_state(self,fsm=None):
        self.state = self.idele
        self.logger.info(f"State: IDLE | Current floor: {self.current_floor}")
        if self.list_floor:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return "MOVING_UP"
            elif next_floor < self.current_floor:
                return "MOVING_DOWN"
       
        
       
        self.sleep_state(fsm)

            
        time.sleep(1)
        return "IDLE"

    def sleep_state(self,fsm):
        # lift = fsm.robot_obj7
        self.logger.info(f"State: Sleep | Current floor: {self.current_floor} fsm in sleep mode")
        self.state = self.sleeping
        fsm.sleep_fsm()
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
        # lift = fsm.robot_obj
        self.state = self.waiting
        self.logger.info(f"Waiting at floor {self.current_floor}")
        if self.list_floor:
            next_floor = next(iter(self.list_floor))
            if next_floor > self.current_floor:
                return "MOVING_UP"
            elif next_floor < self.current_floor:
                return "MOVING_DOWN"
        time.sleep(2)
        return "IDLE"
    def return_to_ground_floor(self):
        self.add_request(0)




    

    # def idle_state(fsm):
    #     lift = fsm.robot_obj
    #     lift.state = lift.idele
    #     lift.logger.info(f"[FSM] State: IDLE | Current floor: {lift.current_floor}")

    #     if lift.list_floor:
    #         next_floor = next(iter(lift.list_floor))
    #         if next_floor > lift.current_floor:
    #             return "MOVING_UP"
    #         elif next_floor < lift.current_floor:
    #             return "MOVING_DOWN"
    #         else:
    #             return "WAITING"

    #     time.sleep(1)
    #     return "IDLE"


    # def moving_up_state(fsm):
    #     lift = fsm.robot_obj
    #     lift.state = lift.moving_up
    #     lift.logger.info(f"[FSM] Moving up from floor {lift.current_floor}")

    #     lift.current_floor += 1
    #     time.sleep(2)

    #     if lift.current_floor in lift.list_floor:
    #         lift.logger.info(f"[FSM] Reached floor {lift.current_floor}")
    #         lift.list_floor.pop(lift.current_floor, None)
    #         return "WAITING"

    #     if not lift.list_floor:
    #         return "IDLE"

    #     next_floor = next(iter(lift.list_floor))
    #     return "MOVING_UP" if next_floor > lift.current_floor else "MOVING_DOWN"


    # def moving_down_state(fsm):
    #     lift = fsm.robot_obj
    #     lift.state = lift.moving_down
    #     lift.logger.info(f"[FSM] Moving down from floor {lift.current_floor}")

    #     lift.current_floor -= 1
    #     time.sleep(2)

    #     if lift.current_floor in lift.list_floor:
    #         lift.logger.info(f"[FSM] Reached floor {lift.current_floor}")
    #         lift.list_floor.pop(lift.current_floor, None)
    #         return "WAITING"

    #     if not lift.list_floor:
    #         return "IDLE"

    #     next_floor = next(iter(lift.list_floor))
    #     return "MOVING_DOWN" if next_floor < lift.current_floor else "MOVING_UP"


    # def waiting_state(fsm):
    #     lift = fsm.robot_obj
    #     lift.state = lift.waiting
    #     lift.logger.info(f"[FSM] Waiting at floor {lift.current_floor}")
    #     time.sleep(2)
    #     return "IDLE"
    

    
   
        



    # def inside_lift(self,step,direction,floor=None):
        
    #     if (step == 1 and direction == "up") or (step == -1 and direction == "down"):
           
    #         self.state=self.waiting
    #         time.sleep(3)
    #         self.update_state("flag_inside_lift",True)
    #         state=self.read_state()
           
            
    #         logger.info(f"current floor :- {floor} and lift state :- {self.waiting}")
            
            
            
    #         if floor:
    #             self.list_floor.pop(floor,None)
    #         # self.update_state("flag_inside_lift",False)

          



    # def move(self):
    #     while self.running:

    #         data=self.read_state()
           
    #         if data.get("floor",0) != 0:
    #             self.add_request(data.get("floor",0))
    #             self.update_state("floor",0)   
    #         with self.lock:
                
    #             if  len(self.list_floor)==0:
    #                 if(self.state != self.idele):
    #                   logger.info(f"current floor :- {self.current_floor} and lift state :- {self.idele}")
    #                   self.state=self.idele
                    
    #                 time.sleep(1)
    #                 continue
              
    #             next_floor, direction = next(iter(self.list_floor.items()))

    #             self.list_floor.pop(next_floor)

    #         step = 1 if next_floor > self.current_floor else -1

    #         if step == 1:
    #            self.list_floor = dict(sorted(self.list_floor.items()))
    #         else:
    #             self.list_floor = dict(sorted(self.list_floor.items(), reverse=True))

            
            
    #         if next_floor== -1:
    #             self.running=False
    #             self.update_state("while_condition",False)
                
    #         if step==1:
    #                 self.state=self.moving_up
    #                 logger.info(f" ======>lift state :- {self.moving_up}")
    #         else:
    #                 self.state=self.moving_down
    #                 logger.info(f"========> lift state :- {self.moving_down}")

           
    #         while self.current_floor != next_floor:
    #             logger.info(f"current floor :- {self.current_floor} ")

                

    #             self.current_floor += step

                

    #             if self.current_floor in self.list_floor:
    #                     direction2=self.list_floor[self.current_floor]
                       
    #                     if direction2 :
    #                         logger.debug(f"direction{direction2}")
    #                         self.inside_lift(step,direction2,self.current_floor)
    #                     else:
    #                         self.state=self.waiting
    #                         logger.info(f"Reached floor {self.current_floor}")
    #                         self.list_floor.pop(self.current_floor)
    #             time.sleep(3)
    #         logger.debug(f"direction{direction} and  {next_floor}")
    #         if direction :
    #             self.inside_lift(step,direction,next_floor)
    #         logger.info(f": Reached floor {self.current_floor}")

    # def return_to_ground_floor(self):
    #     self.add_request(0)



