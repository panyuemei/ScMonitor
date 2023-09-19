from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '人才链测试环境客户端（备案）'
    default_ding_title = '人才链测试环境客户端（备案）告警'
    base_url = 'http://rencai.shangchain.tech:30023/webclient-talent/'
    default_ding_tail_text = '[人才链测试环境客户端（备案）](http://rencai.shangchain.tech:30023/clientWebT/)'
    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_total_info(self):
        self.api_monitor('get', '/portal/home/findTalentData', name='人才链首页数据统计',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30),
                         timeout=50,
                         request_stop_after_attempt=2)
