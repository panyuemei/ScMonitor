from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '玩链科技AI'
    default_ding_title = '玩链科技AI告警'
    base_url = 'https://playchain.straitchain.com/glm-prod-all/'
    default_ding_tail_text = '[玩链科技AI](http://webdev.straitchain.com:8080/glm-prod-all/?id=sdgv)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_api_common_saveViewLog(self):
        self.api_monitor('post','/api/common/saveViewLog',
                         data={"knowledge":"straits-02"},
                         name='保存查看日志',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, assert_data_code=False),
                         timeout=50,
                         request_stop_after_attempt=2)

