from fastapi import APIRouter,HTTPException
import re
import src.manager as manager
from utils.logger import setup_logger

logger=setup_logger("api_request")
logger2=setup_logger("api_response")





router = APIRouter(prefix="/lift", tags=["lift"])



@router.post("/inside-lift")
def inside_lift(floor: int):
    try:
        logger.info(f"Request for floor {floor} inside lift")
        
        if floor == -1:
            manager.stop_fsm()
            logger2.info({"message": "Lift FSM stopped."})
            return {"message": "Lift FSM stopped."}
        
        resp=manager.add_request(floor)
        logger2.info(resp)
        return resp
    
    except ValueError as e:
        logger2.error(f"Value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}") 
        raise HTTPException(status_code=500, detail="Internal server error")
    

# @router.post("/inside-lift")
# def inside_lift(floor: int):
#     try:
#         logger.info(f"request for the {floor} inside lift")
#         if floor == -1:
#             manager.stop_fsm()
#             logger2.info({"message": "Lift FSM stopped."})
#             return {"message": "Lift FSM stopped."}
#         manager.add_request(floor)
#         logger2.info({"message": f"Request added to floor {floor}"})
#         return {"message": f"Request added to floor {floor}"}
#     except Exception as e:
#         raise e



@router.post("/outside-lift")
def outside_lift(floor: str):
    try:
        logger.info(f"request for the {floor} out-side  lift")
        match = re.match(r'^(UP|DOWN)\s*(\d+)$', floor.strip(), re.IGNORECASE)
       
        if not match:
            logger2.error({"error": "Invalid request format. Use 'UP 5' or 'DOWN 3'"})
            raise ValueError("Invalide request format. Use 'UP 5' or 'DOWN 3'")

        direction = match.group(1).upper()
        dest = int(match.group(2))

        if dest < 0:
            raise ValueError(f"Invalide floor number: {dest}. floor must be positive.")
        
        resp= manager.add_request(dest, direction)
        logger2.info({"message": f"Request added to floor {dest} {direction}"})
        return resp
    except ValueError as e:
        logger2.warning({"warning": str(e)})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger2.warning({"warning": str(e)})
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") 

@router.post("/emergency")
def emergency():
    try:
        result = manager.emergency(True)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
   
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
   

@router.post("/resume")
def resume():
    try:
        result = manager.resume(True)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
