import logging
import yaml
import logging.config

class Logger:
    def __init__(self, name=None, log_config_path=None):
        self.name=name
        self.logger=None
        self.log_config_path=log_config_path

    def get_logger(self):
        try:
           with open (self.log_config_path) as f:
               config = yaml.safe_load(f)
        except Exception as e:
            raise e
        logging.config.dictConfig(config)
        self.logger = logging.getLogger(self.name)
        return self.logger

if __name__ == '__main__':
    logger_obj=Logger("kannan",r"C:\Users\navkanna\PycharmProjects\aggregator\aggregator\etc\log_config")
    logger=logger_obj.get_logger()
    logger.info("test")
