from fastapi import APIRouter
import re
from Lift.lift import Lift
import manager
from utils.logger import setup_logger


total_floors = 10 
# lift = Lift(total_floors)

router = APIRouter(prefix="/lift", tags=["lift"])


@router.post("/inside-lift")
def inside_lift(floor: int):
    if floor == -1:
        manager.stop_fsm()
        return {"message": "Lift FSM stopped."}
    manager.add_request(floor)
    return {"message": f"Request added to floor {floor}"}


@router.post("/outside-lift")
def outside_lift(floor: str):
    match = re.match(r'^(UP|DOWN)\s*(\d+)$', floor.strip(), re.IGNORECASE)
    if not match:
        return {"error": "Invalid request format. Use 'UP 5' or 'DOWN 3'"}

    direction = match.group(1).upper()
    dest = int(match.group(2))

    manager.add_request(dest, direction)
    return {"message": f"Request added to floor {dest} ({direction})"}


# @router.post("/emergency-button")
# def emergency_button():
    # lift.list_floor = {}
    # lift.return_to_ground_floor()
    # return {"message": "Emergency! Lift returning to ground floor."}
