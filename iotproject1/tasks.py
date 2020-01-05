
import datetime
import celery
#Celery runs this function once every day
@celery.decorators.periodic_task(run_every=datetime.timedelta(days=1))
def myTask():
    #nightly shift job
    from iotproject1.views import delete_old_requests
    print("REQUESTS OLDER THAN 24 HORUS WILL BE DELETED EVERY DAY AT MIDNIGHT DELETED")
    delete_old_requests()
