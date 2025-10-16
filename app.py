from fastapi import FastAPI
from src.router_lift.lift_router import router 


app = FastAPI(title="Lift Control API")


app.include_router(router)


