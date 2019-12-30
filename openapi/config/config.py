import os
from openapi.utils.common import is_exist_path

class NirvanaConfig(object):

    def postgres_config(self):
        pg_provider = os.getenv('PG_PROVIDER') if  os.getenv('PG_PROVIDER') else 'postgres'
        pg_host = os.getenv('PG_HOST') if os.getenv('PG_HOST') else '127.0.0.1'
        pg_user = os.getenv('PG_USER') if  os.getenv('PG_USER') else 'postgres'
        pg_password = os.getenv('PG_PASSWORD') if  os.getenv('PG_PASSWORD') else '123456'
        pg_database = os.getenv('PG_NAME') if  os.getenv('PG_NAME') else 'nirvana03'
        return pg_provider, pg_host, pg_user, pg_password, pg_database

    def workspace_config(self):
        pass

    def script_save_path(self):
        script_save_path = os.getenv('SCRIPT_SAVE_PATH') if  os.getenv('SCRIPT_SAVE_PATH') else f'{os.getcwd()}/openapi/script'
        return script_save_path

    def report_save_path(self):
        report_save_path = os.getenv('REPORT_SAVE_PATH') if  os.getenv('REPORT_SAVE_PATH') else f'{os.getcwd()}/openapi/report'
        return report_save_path

    def report_ip(self):
        report_ip = os.getenv('REPORT_IP') if  os.getenv('REPORT_IP') else f'http://127.0.0.1:9090'
        return report_ip


def check_config_path():
    script_save_path = NirvanaConfig().script_save_path()
    is_exist_path(script_save_path)
    report_save_path = NirvanaConfig().report_save_path()
    is_exist_path(report_save_path)