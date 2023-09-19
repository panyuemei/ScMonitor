from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '玩链科技AI-管理后台'
    default_ding_title = '玩链科技AI-管理后台告警'
    base_url = 'https://playchain.straitchain.com/glm-prod-all/'
    default_ding_tail_text = '[玩链科技AI-管理后台](https://playchain.straitchain.com/admin/)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_api_common_saveViewLog(self):
        self.api_monitor('get', '/backend/common/getBackendData?knowledge=straits-02',
                         name='获取Backend数据',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, assert_data_code=False),
                         timeout=50,
                         request_stop_after_attempt=2)

