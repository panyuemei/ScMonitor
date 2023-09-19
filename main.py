import importlib
import logging
import os
import sys
import toml
from apscheduler.schedulers.blocking import BlockingScheduler
from common.monitor import BaseMonitor

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s')
logger = logging.getLogger()
env = sys.argv[1] if len(sys.argv) > 1 else 'dev'
config = toml.load(f'./conf/config-{env}.toml')
logger.info(f'加载配置文件[{env}]：{config}')
logger.setLevel(config['log']['level'])

def live_notification(names):
    logging.info(f'监控存活通知{names}')
    content = '**监控任务正在运行中：**\n- ' + '\n- '.join(names)
    BaseMonitor(config).ding(content, title='监控存活通知')

def job(module):
    logging.info(f'开始执行任务：{module.Monitor.title}')
    module.Monitor(config).exec()
    logging.info(f'任务执行结束：{module.Monitor.title}')

def main():
    scheduler = BlockingScheduler()
    tasks_name = pick_tasks if (pick_tasks := config['monitor'].get('pick_tasks')) and env == 'dev' else [i[:-3] for i
                                                                                                          in os.listdir(
            './tasks') if not i.startswith('_') and i.endswith('.py') and i[:-3] not in config['monitor']['omit_tasks']]
    tasks_name_title = []
    for task_name in tasks_name:
        module = importlib.import_module(f'tasks.{task_name}')
        kwargs = {**config['scheduler'], **module.Monitor.scheduler_kwargs}
        tasks_name_title.append(module.Monitor.title)
        scheduler.add_job(job, args=[module], name=task_name, **kwargs)
    if not config['live_notification'].get('disable'):
        scheduler.add_job(lambda: live_notification(tasks_name_title), name='监控存活通知',
                          **config['live_notification']['scheduler'])
        live_notification(tasks_name_title)
    scheduler.start()
main()

















