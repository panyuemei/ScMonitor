from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '数字人-wcb'
    default_ding_title = '数字人-wcb告警'
    base_url = 'https://passn.shang-chain.com/webclient/'
    default_ding_tail_text = '[数字人-wcb](https://pass.shang-chain.com/introduce/)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_api_common(self):
        self.api_monitor('get', '/api/straitChain/getRoom',
                         name='获取展厅地址',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=50,
                         request_stop_after_attempt=2)
