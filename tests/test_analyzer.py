import os.path
from datetime import date

from src.analyzer import NginxLogAnalyzer, NginxLogFile
from src.config import Settings
from tests.utils import create_temp_file, delete_temp_file


class TestAnalyzer:

    settings = Settings()
    analyzer = NginxLogAnalyzer(settings)

    def _check_last_nginx_log(self, nginx_log_file, last_log_expected):
        create_temp_file(nginx_log_file)

        print(last_log_expected)
        last_log = self.analyzer.find_last_nginx_log_file()
        print(last_log)
        delete_temp_file(nginx_log_file)
        return last_log_expected == last_log

    def test_find_last_nginx_log_file_without_extension(self):
        """Test last log without extension"""
        temp_file_path = "./log/nginx-access-ui.log-20300630"
        last_log_expected = NginxLogFile(
            path=os.path.abspath(temp_file_path),
            date=date(2030, 6, 30),
            extension="",
        )
        assert self._check_last_nginx_log(temp_file_path, last_log_expected)

    def test_find_last_nginx_log_file_gz(self):
        """Test gz last log"""
        temp_file_path = "./log/nginx-access-ui.log-20300630.gz"
        last_log_expected = NginxLogFile(
            path=os.path.abspath(temp_file_path),
            date=date(2030, 6, 30),
            extension=".gz",
        )
        assert self._check_last_nginx_log(temp_file_path, last_log_expected)

    def test_find_last_nginx_log_file_not_bz2(self):
        """Test gz last log"""
        temp_file_path = "./log/nginx-access-ui.log-20300630.gz"
        uncorrect_temp_file_path = "./log/nginx-access-ui.log-20300630.bz2"
        create_temp_file(uncorrect_temp_file_path)
        last_log_expected = NginxLogFile(
            path=os.path.abspath(temp_file_path),
            date=date(2030, 6, 30),
            extension=".gz",
        )
        delete_temp_file(uncorrect_temp_file_path)
        assert self._check_last_nginx_log(temp_file_path, last_log_expected)
