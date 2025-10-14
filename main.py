import threading
from Lift.lift import Lift
import re
import time 
from fastapi import FastAPI
from pydantic import BaseModel 
from fsm import FSM
from Lift.lift import Lift

from utils.logger import setup_logger



total_floors = int(input("Enter total floors in the building: "))
lift = Lift(total_floors)
fsm = FSM("LiftFSM", robot_obj=lift, logger=setup_logger("fsm"))


fsm.add_state("IDLE", "IDLE", lambda: lift.idle_state(fsm))
fsm.add_state("MOVING_UP", "MOVING_UP", lambda: lift.moving_up_state())
fsm.add_state("MOVING_DOWN", "MOVING_DOWN", lambda: lift.moving_down_state())
fsm.add_state("WAITING", "WAITING", lambda: lift.waiting_state())
fsm.add_state("SLEEPING", "SLEEPING", lambda: lift.sleep_state())

fsm.set_current_state("IDLE")
fsm.start_fsm_thread()




app=FastAPI()



@app.post("/inside-lift",tags=["lift"])
def inside_left(floor:int):
    dest=floor
    if dest == -1 :
         fsm.stop()
    if dest <-1:
            return { dest:" invalide floor "}
    lift.add_request(dest,fsm=fsm)
    return {"message": f"Request added to floor {dest}"}


@app.post("/outside-lift",tags=["lift"])
def outside_lift(floor:str):
    match = re.match(r'^(UP|DOWN)\s*(\d+)$', floor.strip(), re.IGNORECASE)
    if match:
        direction = match.group(1)
        dest = int(match.group(2))
        if dest <-1:
            return { dest:" invalide floor "}
    lift.add_request(dest, direction,fsm=fsm)
    return {"message": f"Request added to floor {dest}"}


@app.post("/emergency-button",tags=["lift"])
def emergency_button():
   
    lift.list_floor = {}
    lift.return_to_ground_floor()
    return {"message": "emergecy exit at ground floor "}



