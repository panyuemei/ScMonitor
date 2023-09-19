from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '夸父'
    default_ding_title = '夸父告警'
    base_url = 'http://47.113.102.228/kfclient/'
    default_ding_tail_text = '[夸父](http://47.113.102.228/kf/)'
    scheduler_kwargs = {
        'seconds': 0,
        'hours': 1
    }

    def monitor_login(self):
        self.api_monitor('post', '/login',
                         data={
                             "username": "admin",
                             "password": "wrong_password"
                         },
                         name='登录',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=60,
                         request_stop_after_attempt=2)
