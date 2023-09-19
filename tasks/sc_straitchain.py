from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '海峡链官网'
    default_ding_title = '海峡链官网告警'
    base_url = 'https://www.straitchain.com/webclient'
    default_ding_tail_text = '[海峡链官网](https://www.straitchain.com/)'


    def monitor__app_market_page(self):
        self.api_monitor('post','/app/market/page',
                    data={
                         'curPage':1,
                         'limit':8,
                         'appType':["consulting"],
                         'keyWord':""},
                     name='开发者服务',
                     use_default_assert=False,
                     assert_func=lambda x: self.default_api_monitor_assert(x, assert_data_code=False),
                     timeout=50,
                     request_stop_after_attempt=2
                         )

