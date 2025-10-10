# from Lift.lift import Lift
import json
import time 


STATE_FILE = "data/shared_state.json"



def read_state():
   
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        
        print("===================================file is not found===================================")



def update_state(key, value):
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except FileNotFoundError:
        print("===================================file is not found===================================")

    state[key] = value
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

if __name__ == "__main__":
    

    while True:
      
        state = read_state()
       
        while_condition = state.get("while_condition", True)
        if not while_condition:
            break
        flag_inside_lift = state.get("flag_inside_lift", False)
        if flag_inside_lift:
            user_input =input("enter floor (inside lift) :- ").strip()
            update_state("floor", int(user_input))
            update_state("flag_inside_lift",False)

        time.sleep(0.5)
