#!/usr/bin/python3
import asyncio
from collections import deque
from datetime import datetime as dt
from datetime import timezone as tz

import psutil

from config.config import Config
from helpers.smtp_sender import SmtpSender
from periodics.send_file_content import set_periodics


class SmtpMonit:
    def __init__(self):
        self.config = Config()
        self.smtp_sender = SmtpSender()
        self.avg_load = None
        self.utils_to_monit = None
        self.alarm_status = None
        self.machine_name = self.config.get_params_config().get('machine_name', '')

    async def main(self):
        if self.utils_to_monit is None:
            self.utils_to_monit = self.config.get_params_config().get('utils_to_monit', '').split(' ')
        if self.avg_load is None:
            self.avg_load = {k: deque([]) for k in self.utils_to_monit}
        if self.alarm_status is None:
            self.alarm_status = {k: True for k in self.utils_to_monit}
        for util in self.avg_load.keys():
            asyncio.create_task(self.change_status(util))
        await set_periodics(periodics=self.config.get_periodics_config(), smtp_sender=self.smtp_sender,
                            machine_name=self.machine_name)
        while True:
            params = self.get_params()
            for k in self.avg_load.keys():
                if len(self.avg_load[k]) < int(self.config.get_params_config().get('intervals_avg_load', '60')):
                    self.avg_load[k].append(params[k])
                else:
                    self.avg_load[k].popleft()
                    self.avg_load[k].append(params[k])
                if not self.alarm_status[k]:
                    await self.send_alarm(util=k)
            await asyncio.sleep(int(self.config.get_params_config().get('checking_interval', '1')))

    async def send_alarm(self, util):
        threshold = sum(self.avg_load[util]) / len(self.avg_load[util])
        if threshold > int(self.config.get_params_config().get(util, '')):
            subject = f'{self.machine_name} ALARM {util}, {threshold:0.2f}%'
            content = dt.now(tz=tz.utc).isoformat()
            await self.smtp_sender.send_message(subject=subject, content=content)
            asyncio.create_task(self.change_status(util))

    async def change_status(self, util):
        self.alarm_status[util] = True
        await asyncio.sleep(int(self.config.get_params_config().get('pause_between_alarm', '600')))
        self.alarm_status[util] = False

    @staticmethod
    def get_params() -> dict:
        memory = psutil.virtual_memory()
        return_params = {'cpu': psutil.cpu_percent(interval=None), 'disk': psutil.disk_usage('/').percent,
                         'memory': (1 - memory.available / memory.total) * 100}
        return return_params


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(SmtpMonit().main())
