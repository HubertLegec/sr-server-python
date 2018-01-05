import logging


class LogFactory:
    ROOT_LOGGER_NAME = 'file_server'
    FORMATTER = logging.Formatter('[%(asctime)s - %(name)s] %(levelname)s : %(message)s')
    DEFAULT_LOG_LEVEL = 'INFO'
    DEFAULT_LOG_FILE = 'logs'
    log = None

    @classmethod
    def get_logger(cls, **kwargs):
        if cls.log:
            return cls.log
        cls.log = logging.getLogger(cls.ROOT_LOGGER_NAME)
        cls.log.setLevel(logging.DEBUG)
        fh = cls._get_file_logger(kwargs)
        ch = cls._get_console_logger(kwargs)
        if fh:
            cls.log.addHandler(fh)
        if ch:
            cls.log.addHandler(ch)
        return cls.log

    @classmethod
    def _get_file_logger(cls, kwargs):
        if 'file_logs' in kwargs and kwargs['file_logs'] == 'yes':
            log_level = cls.DEFAULT_LOG_LEVEL
            if 'file_log_level' in kwargs and kwargs['file_log_level']:
                log_level = kwargs['file_log_level']
            log_file = cls.DEFAULT_LOG_FILE
            if 'log_file' in kwargs and kwargs['log_file']:
                log_file = kwargs['log_file']
            log = logging.FileHandler(log_file)
            log.setLevel(log_level)
            log.setFormatter(cls.FORMATTER)
            return log
        return None

    @classmethod
    def _get_console_logger(cls, kwargs):
        if 'console_logs' in kwargs and kwargs['console_logs'] == 'no':
            return None
        log_level = cls.DEFAULT_LOG_LEVEL
        if 'console_log_level' in kwargs and kwargs['console_log_level']:
            log_level = kwargs['console_log_level']
        log = logging.StreamHandler()
        log.setLevel(log_level)
        log.setFormatter(cls.FORMATTER)
        return log
