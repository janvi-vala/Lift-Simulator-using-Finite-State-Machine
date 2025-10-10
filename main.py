import threading
from Lift.lift import Lift
import re
import json
import time 


total_floors = int(input("Enter total floors in the building: "))

lift = Lift(total_floors)









while lift.running:
    user_input = input(
        f"Current floor: {lift.current_floor}. Enter destination floor "
        "(or -1 to exit, blank to return to ground floor): "
    ).strip()

    if user_input == "":
        lift.return_to_ground_floor()
        continue

    try:

        match = re.match(r'^(UP|DOWN)\s*(\d+)$', user_input.strip(), re.IGNORECASE)
        if match:
            direction = match.group(1)
            dest = int(match.group(2))
       
        else:
            dest = int(user_input)

        if dest == -1:
            lift.running = False
            lift.update_state("while_condition", False)

            print("Exiting lift simulator.")
            break
        
        if match:
            lift.add_request(dest, direction)
        else:
            lift.add_request(dest)
    except ValueError:
        print("Please enter a valid floor number.")
    time.sleep(0.5)
