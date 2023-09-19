from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = 'TraceDemo'
    default_ding_title = 'TraceDemo告警'
    base_url = 'https://liu.chain-meeting.com/tracedemo/'
    default_ding_tail_text = ''
    scheduler_kwargs = {
        'seconds': 0,
        'hours': 1
    }

    def monitor_live(self):
        self.api_monitor('get', '/not_exist_api',
                         name='服务存活',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=60,
                         request_stop_after_attempt=2)
