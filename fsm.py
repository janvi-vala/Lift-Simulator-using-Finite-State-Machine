import sys
import traceback
from threading import Event
from threading import Thread
# import settings


class FSM(object):
    FSM_STATUS_RUN = 1
    FSM_STATUS_PAUSE = 2
    FSM_STATUS_SLEEP = 0
    FSM_STATUS_WAKE = 1

    def __init__(self, name, robot_obj, logger=None):

        self.name = name  # just a name
        self.robot_obj = robot_obj
        self.state_routine_map = {}  # a map which contains a next state (default is current state) and a state_routine
        self.current_state = None  # holds the current state
        self.old_state = None
        self.new_requested_state = None

        #flags
        self.exit_requested = False  # used to exit the thread
        self.standby = False
        self.fsm_stopped = False
        self.current_status = 1
        self.sleep_status = 1
      
        self.fsm_logger = logger
        self.fsm_thread = None
       
        self.event = Event()
        self.sleep_time = 0

    def add_state(self, state, default_next_state, routine):
        """
        To Add state into FSM, before add state make sure you define handler function for the same state

        :param state: current state which is running
        :param default_next_state: default state if any thing wrong happened in current state
        :param routine: handler for the current state
        :return: NULL
        """
        self.state_routine_map[state] = (default_next_state, routine)

    def set_current_state(self, state):
        """
        To set state in running FSM

        :param state: which state want to set as current state.
        :return: NULL
        """
        if self.fsm_logger:
            self.fsm_logger.info("FSM: set_current_state - current_state = " + str(state) + " from: " + str(self.current_state))
        self.new_requested_state = state
        if state == 'Standby':
            self.standby = True

    def start_fsm(self, run_only_once=False):
        """
        It will start FSM which is set in default state

        :param run_only_once: If we don't want to run fsm continuously then we set this flag True
        :return: None
        """
        self.robot_obj.logger.info("{} started".format(self.name))
        try:
            self.fsm_stopped = False
            while not self.exit_requested:
                if self.current_status == self.FSM_STATUS_RUN:
                    self.reset_event()
                    self.set_sleep_time(timeout=0)
                    if self.new_requested_state is not None:
                        self.current_state = self.new_requested_state
                        self.new_requested_state = None
                    if not len(self.state_routine_map):
                        # as long as there are some state
                        # the thread is alive
                        break
                    func = self.state_routine_map[self.current_state][1]
                    if self.old_state != self.current_state:
                        self.fsm_logger.info("FSM: " )
                    next_state = func()
                    self.old_state = self.current_state
                    if self.new_requested_state is None:
                        if next_state is not None:
                            self.current_state = next_state
                        else:
                            self.current_state = self.state_routine_map[self.current_state][0]
                    else:
                        self.current_state = self.new_requested_state
                        self.new_requested_state = None

                    self.sleep_fsm(timeout=self.sleep_time)
                else:
                    pass

                if run_only_once:
                    break
            self.fsm_stopped = True
        except Exception:
            # self.fsm_stopped = True
            # self.robot_obj.update_error_document(fsm_error=settings.ROBOT_CODES["ROBOT_CODE_FAILURE"])
            # self.robot_obj.send_notification_data(station_type=settings.ROBOT_STATION_TYPE,
            #                                        error_code=settings.ROBOT_CODES["ROBOT_CODE_FAILURE"],
            #                                        station_name=settings.GOOGLE_HOME_STATION_NAME["ROBOT"],
            #                                        logger=self.robot_obj.logger)
            # self.robot_obj.logger.exception("")
            # self.robot_obj.logger.error("******* {} Failure *******".format(self.name))
            if self.fsm_logger:
                self.fsm_logger.exception("FSM: start_fsm - error in fsm thread execution")
            else:
                traceback.print_exc(file=sys.stdout)
                self.sleep_fsm()

    def stop(self):
        """
        It will stop the FSM

        :return: NULL
        """
        self.exit_requested = True
        self.name = ''

    def stand_by(self):
        """
        To put FSM in stand by mode

        :return: NULL
        """
        pass

    def start_fsm_thread(self):
        self.fsm_thread = Thread(target=self.start_fsm, name=self.name)
        self.fsm_thread.setDaemon(True)
        self.fsm_thread.start()

    def reset_event(self):
        self.event.clear()

    def set_sleep_time(self, timeout=None):
        """
        timeout -> 0 for no wait , None for infinite wait
        """
        self.sleep_time = timeout

    def sleep_fsm(self, timeout=None):
        # self.fsm_logger.info("SLEEP CALLED")
        # self.event.clear()
        self.event.wait(timeout)

    def wake_up(self):
        # self.fsm_logger.info("WAKEUP CALLED")
        self.event.set()
