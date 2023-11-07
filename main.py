from application.application_class import ASLDetectorApp
import time
from application.database.json_manager import JsonManager


if __name__ == '__main__':

    time_init = time.time()
    
    ASLDetectorApp().run()
    
    running_time = time.time() - time_init
    JsonManager().add_execution_time(running_time)