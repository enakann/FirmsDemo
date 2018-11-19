
from utils import DataStore
from utils import Logger
logger_obj=Logger("aggregator","log_config.yml")
logger=logger_obj.get_logger()

logger.info("Starting database transactions")

with DataStore (r"C:\Users\navkanna\PycharmProjects\FirmsDemo\Aggregator\Aggregator\test.db") as dbobj:
    ret = dbobj.select_data ("select * from contacts where first_name=:1", ("nav",))
    print (ret)
