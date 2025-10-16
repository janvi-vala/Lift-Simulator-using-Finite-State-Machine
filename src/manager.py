
import os
from dotenv import load_dotenv
from src.lift import Lift
from fastapi import HTTPException,status
from utils.logger import setup_logger


load_dotenv()
total_floors = int(os.getenv("total_floor"))
lift = Lift(total_floors)
logger=setup_logger("api_request")
logger2=setup_logger("api_response")

def stop_fsm():
     lift.stop()

def add_request(floor, direction=None,fsm=None):
    try:
        with lift.lock:
        
            if 0 <= floor <= lift.total_floors:
                
                if floor not in lift.list_floor and lift.current_state != "EMERGENCY":
                    lift.list_floor[floor] = direction
                elif lift.FLAG_RESUME == True :
                     lift.logger.info(f"first Resume lift first")
                     return {"status":"Failure","detail":"First resume the lift"}
                
            
                if lift.current_state == "IDLE":
                
                    lift.wake_up()
                    lift.logger.info(f"Lift wake up from the sleep current floor is {lift.current_floor}")
                if direction:
                    return  {"message": f"Request added to floor {floor} and {direction}"}
                else :
                     return  {"message": f"Request added to floor {floor}"}

            else:
                lift.logger.error(f"Lift Invalid floor {floor}")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="entered floor is invalid")
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

def return_to_ground_floor(self):
    add_request(0)

def emergency(emergency_flag: bool):
    try:
        if not emergency_flag:
            raise ValueError("Invalid emergency flag value")

      
        if lift is None:
            raise RuntimeError("Lift instance not initialized")

        # lift.list_floor = {}
        lift.FLAG_RESUME=True
        lift.logger.info("Emergency mode activated.")

        return {"status": "success", "message": "Lift is entered in the emergency mode"}

    except Exception as e:
        logger.exception("Error in emergency function: {}".format(str(e)))
        raise HTTPException(status_code=500, detail=f"Emergency activation failed: {e}")

def resume(flag: bool):
    try:
        if not flag:
            raise ValueError("invalide resume flag value")

        if lift is None:
            raise RuntimeError("Lift instance not initialized")

   

  
        if lift.current_state != "WAITING":
            logger.warning("Resume called when lift not in emergency state.")
            return {"status": "warning", "message": "lIFT IS NOT IN EMERGENCY SO RESUME IS IGNORE"}
        
        lift.list_floor = {}
        lift.FLAG_RESUME=True
      

        lift.logger.info("Lift resumed from emergency.")
        logger.info("Lift successfully resumed from emergency.")
        lift.wake_up()
        return {"status": "success", "message": "Lift resumed successfully"}

    except Exception as e:
        logger.exception("ERROR  in resume function: %s", e)
        raise HTTPException(status_code=500, detail=f"Resume failed: {e}")


          
          