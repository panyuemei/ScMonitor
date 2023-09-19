from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '海峡链Pass小程序'
    default_ding_title = '海峡链Pass小程序告警'
    base_url = 'https://passn.shang-chain.com/webclient'

    def monitor_login_by_username(self):
        self.api_monitor('post', '/login', data={'username': '16000000000', 'password': ''}, name='手机号登录')

    def monitor_collection_page(self):
        self.api_monitor('post',
                         '/collectionItem/page',
                         data={'curPage': 1, 'limit': 10, 'collectSn': None},
                         headers={
                             'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdHJhaXQtY2hhaW4tcGFzc19vZmZpY2lhbCIsImNsaWVudCI6IjE4ODE1NTk2OTYzIiwidXNlcklkIjoxODUsInVuaW9uSWQiOiIxNTI2MTY1NzAxMTIxOTM3NDA4IiwiaWF0IjoxNjc2ODg0ODE5LCJleHAiOjE2Nzc1MzI4MTl9.gBUfUWwxlIyrS9fvdRi7J_2uLvap6QwGiLvTqqoFMjQ'},
                         name='藏品列表',
                         use_default_assert=False,
                         assert_func=lambda x: self.default_api_monitor_assert(x, assert_data_code=False))
