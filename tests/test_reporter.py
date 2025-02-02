from src.analyzer import NginxLogAnalyzer
from src.config import Settings
from src.reporter import Reporter
from tests.utils import create_temp_file, delete_temp_file

TEST_LOG = (
    '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9'
    ' libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390\n'
    '1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET /api/1/photogenic_banners/list/?server_name=WIN7RB'
    '4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" 0.133\n'
    '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/16852664 HTTP/1.1" 200 19415 "-" "Slotovod" '
    '"-" "1498697422-2118016444-4708-9752769" "712e90144abee9" 0.199'
    '1.199.4.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/slot/4705/groups HTTP/1.1" 200 2613 "-" "Lynx/2.8.8dev.9'
    ' libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-3800516057-4708-9752745" "2a828197ae235b0b3cb" 0.704\n'
    '1.168.65.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/internal/banner/24294027/info HTTP/1.1" 200 407 "-" "-"'
    ' "-" "1498697422-2539198130-4709-9928846" "89f7f1be37d" 0.146\n'
    '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/group/1769230/banners HTTP/1.1" 200 1020 "-"'
    ' "Configovod" "-" "1498697422-2118016444-4708-9752747" "712e90144abee9" 0.628\n'
    '1.194.135.240 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/group/7786679/statistic/sites/?date_type=day&date_'
    'from=2017-06-28&date_to=2017-06-28 HTTP/1.1" 200 22 "-" "python-requests/2.13.0" "-" "1498697422-3979856266-4708-'
    '9752772" "8a7741a54297568b" 0.067\n'
    '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/1717161 HTTP/1.1" 200 2116 "-" "Slotovod" "-"'
    ' "1498697422-2118016444-4708-9752771" "712e90144abee9" 0.138'
)


TEST_REPORT_DATA = [
    {
        "url": "/api/v2/banner/16852664",
        "count": 1,
        "time_sum": 0.704,
        "time_max": 0.704,
        "time_med": 0.704,
        "time_avg": 0.704,
        "count_perc": 14.285714285714285,
        "time_perc": 31.912964641885765,
    },
    {
        "url": "/api/v2/group/1769230/banners",
        "count": 1,
        "time_sum": 0.628,
        "time_max": 0.628,
        "time_med": 0.628,
        "time_avg": 0.628,
        "count_perc": 14.285714285714285,
        "time_perc": 28.467815049864008,
    },
    {
        "url": "/api/v2/banner/25019354",
        "count": 1,
        "time_sum": 0.39,
        "time_max": 0.39,
        "time_med": 0.39,
        "time_avg": 0.39,
        "count_perc": 14.285714285714285,
        "time_perc": 17.679057116953764,
    },
    {
        "url": "/api/v2/internal/banner/24294027/info",
        "count": 1,
        "time_sum": 0.146,
        "time_max": 0.146,
        "time_med": 0.146,
        "time_avg": 0.146,
        "count_perc": 14.285714285714285,
        "time_perc": 6.618313689936536,
    },
    {
        "url": "/api/v2/banner/1717161",
        "count": 1,
        "time_sum": 0.138,
        "time_max": 0.138,
        "time_med": 0.138,
        "time_avg": 0.138,
        "count_perc": 14.285714285714285,
        "time_perc": 6.255666364460563,
    },
    {
        "url": "/api/1/photogenic_banners/list/?server_name=WIN7RB4",
        "count": 1,
        "time_sum": 0.133,
        "time_max": 0.133,
        "time_med": 0.133,
        "time_avg": 0.133,
        "count_perc": 14.285714285714285,
        "time_perc": 6.029011786038079,
    },
    {
        "url": "/api/v2/group/7786679/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28",
        "count": 1,
        "time_sum": 0.067,
        "time_max": 0.067,
        "time_med": 0.067,
        "time_avg": 0.067,
        "count_perc": 14.285714285714285,
        "time_perc": 3.0371713508612874,
    },
]


class TestReporter:

    settings = Settings()
    analyzer = NginxLogAnalyzer(settings)

    def test_make_report_data(self):
        """Test make report data"""
        temp_file_path = "./log/nginx-access-ui.log-20300630"
        create_temp_file(temp_file_path, TEST_LOG)
        last_log = self.analyzer.find_last_nginx_log_file()
        logs = self.analyzer.get_nginx_logs(last_log)
        reporter = Reporter(self.settings, last_log)
        report_data = reporter.make_report_data(logs)
        delete_temp_file(temp_file_path)
        assert report_data == TEST_REPORT_DATA
