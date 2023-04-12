import DB as db
import pandas as pd
import decouple
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

config = decouple.AutoConfig(' ')
main_data_path = config('PATH_MY_MAIN_DATA')
tickers = list(pd.read_csv(main_data_path + 'tickers.csv', index_col='Unnamed: 0')['ticker'])

def test():
    print('Hello World')
    
def main():
    scheduler1 = BackgroundScheduler()
    scheduler2 = BackgroundScheduler()
    scheduler3 = BackgroundScheduler()
    
    trigger1 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="6", minute="30", second="30"
    )
    
    trigger2 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="10", minute="15"
    )
    
    trigger3 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="12", minute="58"
    )
    
    scheduler1.add_job(
        db.upload_data,
        trigger=trigger1,
        misfire_grace_time=5,
        args=[tickers],
        name="open",
    )
    
    scheduler2.add_job(
        db.upload_data,
        trigger=trigger2,
        misfire_grace_time=5,
        args=[tickers],
        name="mid",
    )
    
    scheduler3.add_job(
        db.upload_data,
        trigger=trigger3,
        misfire_grace_time=5,
        args=[tickers],
        name="close",
    )
    
    trigger4 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="22", minute="18", second="30"
    )
    
    trigger5 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="22", minute="19"
    )
    
    trigger6 = CronTrigger(
        year="*", month="*", day_of_week='mon-fri', hour="22", minute="20"
    )
    
#    scheduler.add_job(
#        test,
#        trigger=trigger4,
#        args=[],
#        name="open",
#    )

    
  
    
    scheduler1.start()
    scheduler2.start()
    scheduler3.start()
    
    while True:
        continue
        
if __name__ == "__main__":
    main()

