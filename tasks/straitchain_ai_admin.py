from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '海峡链AI-管理后台'
    default_ding_title = '海峡链AI-管理后台告警'
    base_url = 'https://glm.straitchain.com/chatglm/'
    default_ding_tail_text = '[海峡链AI-管理后台](https://glm.straitchain.com/admin)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_api_common(self):
        self.api_monitor('get', '/common/getBackendData',
                         data={},
                         name='获取Backend数据',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=50,
                         request_stop_after_attempt=2)