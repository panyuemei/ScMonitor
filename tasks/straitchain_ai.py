from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '海峡链AI'
    default_ding_title = '海峡链AI告警'
    base_url = 'https://glm.straitchain.com/chatglm/'
    default_ding_tail_text = '[海峡链AI](https://glm.straitchain.com/chat)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_api_common(self):
        self.api_monitor('post', '/user/loginBySms',
                         data={'mobile': "19985751513", 'code': "984711"},
                         name='登录',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=50,
                         request_stop_after_attempt=2)
