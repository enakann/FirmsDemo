#
# A wrapper for Python logging module.
#
import sys
import os
import json
import traceback
import logging
import logging.config
import textwrap


class Logger (object):
    """

    Logger base class adding verbose logging to subclasses.

    synopsis:

        import log
        logger = log.Logger( name          =   "<logger_name>",
                             config_path   =   "<path to json config file>" )
        logger.info('It Works')

    description:

        Class methods info(), debug(), error(), fatal() alongside
        the information provided, also shows other useful details
        such as caller details, timestamp etc.

        Log entries would be in the below format:
            col1  col2  col3 ... col6
	where:
            col1 => <logger_name>
            col2 => <timestamp>
            col3 => <called_module>::<called_func>
            col4 => <level>
            col5 => <process_id>
            col6 => (<calling_file>::<line_no>)::<calling_func>
            col7 => message
    """
    
    def __init__(self, name=None, config_path=None, log_file=None):
        
        """
          : constructor for class Logger
          : raise exception if logger name is not passed
          : raise exception if config_path is not passed

        """
        
        if name is None:
            raise ValueError ("Mandatory param 'name' is missing while instantiating 'Logger'")
        
        if config_path is None:
            raise ValueError ("Mandatory param 'config_path' is missing while instantiating 'Logger'")
        
        self.name = name
        
        self.config_path = config_path
        
        self.log_file = log_file
        
        self.__get_logger (self.name)
    
    def __get_logger(self, name=None):
        
        """
          : read json logging config file
          : create logger object

        """
        
        config = read_json_file (self.config_path)
        
        if self.log_file is not None:
            
            if os.path.exists (os.path.dirname (self.log_file)):
                config['handlers'][name]['filename'] = self.log_file
            else:
                raise IOError ("log file {} cannot be created.".format (self.log_file))
        
        logging.config.dictConfig (config);
        
        logger = logging.getLogger (self.name)
        
        self.logger = logger
    
    def _formatter(self, log_fn, message, exc_info):
        
        """
             Formats the message as needed and calls the correct logging method
             to handle it
        """
        
        # Variables
        loc = ''
        fn = ''
        
        # Constants
        TRACEBACK_STACK = -3
        FILE_NAME = 0
        LINE_NO = 1
        FUNC_NAME = 2
        
        tb = traceback.extract_stack ()
        
        if len (tb) > 2:
            
            loc = '(%s:%d)::' % (os.path.basename (tb[TRACEBACK_STACK][FILE_NAME]),
                                 tb[TRACEBACK_STACK][LINE_NO])  # calling file name and line number
            
            fn = tb[TRACEBACK_STACK][FUNC_NAME]  # calling function name
            
            if fn != '<module>':
                fn += '()'
        
        log_fn (loc + fn + ' - ' + message, exc_info=exc_info)
    
    def info(self, message, exc_info=False):
        
        """
            Log a info-level message. If exc_info is True, if an exception
            was caught, show the exception information (message and stack trace)
        """
        self._formatter (self.logger.info, message, exc_info)
    
    def debug(self, message, exc_info=False):
        
        """
            Log a debug-level message. If exc_info is True, if an exception
            was caught, show the exception information (message and stack trace)
        """
        
        self._formatter (self.logger.debug, message, exc_info)
    
    def error(self, message, exc_info=False):
        
        """
            Log a error-level message. If exc_info is True, if an exception
            was caught, show the exception information (message and stack trace)
        """
        
        self._formatter (self.logger.error, message, exc_info)
    
    def fatal(self, message, exc_info=False):
        
        """
            Log a critical-level message. If exc_info is True, if an exception
            was caught, show the exception information (message and stack trace)
        """
        
        self._formatter (self.logger.fatal, message, exc_info)


def read_json_file(path):
    """
      read json file and raise exception in case of any error
    """
    
    try:
        with open (path, 'rt') as f:
            data = json.load (f)
    
    except IOError as e:
        raise
    
    else:
        return data


if __name__ == '__main__':
    print
    Logger.__doc__;

