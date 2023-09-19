from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '海峡链管理后台'
    default_ding_title = '海峡链管理后台告警'
    base_url = 'https://scadmin.straitchain.com/webadmin'
    default_ding_tail_text = '[海峡链管理后台](https://scadmin.straitchain.com/)'
    # scheduler_kwargs = {
    #     'seconds': 0,
    #     'hours': 1
    # }

    def monitor__app_market_page(self):
        self.api_monitor('post','/login',
                     data={
                         "username":"sys",
                         "password":"qwe123"},

                     name='登录',
                     use_default_assert=False,
                     assert_func=lambda x: self.default_api_monitor_assert(x, assert_data_code=False),
                     timeout=50,
                     request_stop_after_attempt=2
                         )

