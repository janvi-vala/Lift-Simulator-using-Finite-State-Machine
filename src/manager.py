from lift import Lift


total_floor=10
lift=Lift(total_floor)

def stop_fsm():
     lift.stop()
def add_request(floor, direction=None,fsm=None):
       
        with lift.lock:
            if 0 <= floor <= lift.total_floors:
                
                if floor not in lift.list_floor:
                    lift.list_floor[floor] = direction
                if lift.state==lift.sleeping:
                    fsm.wake_up()
                
            else:
                lift.logger.error(f"Lift Invalid floor {floor}")

def return_to_ground_floor(self):
        self.add_request(0)