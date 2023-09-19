from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '海峡链节点管理后台'
    default_ding_title = '海峡链节点管理后台告警'
    base_url = 'https://admin.straitchain.com/webadmin'
    default_ding_tail_text = '[海峡链节点管理后台](https://admin.straitchain.com/)'
    # scheduler_kwargs = {
    #     'seconds': 0,
    #     'hours': 1
    # }

    def monitor_login(self):
        self.api_monitor('post', '/login',
                         data={
                             "username": "1669971502@qq.com",
                             "password": "wrong_password"
                         },
                         name='登录',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, 30, False),
                         timeout=60,
                         request_stop_after_attempt=2)
