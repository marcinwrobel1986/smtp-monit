import aiofiles

from periodics.periodic_callback import PeriodicCalllback


async def _get_file_content(file):
    async with aiofiles.open(file, mode='r') as f:
        content = await f.read()
        return content


async def _send_file_content(file: str, smtp_sender, machine_name: str, description: str):
    content = await _get_file_content(file=file)
    subject = f'{machine_name} {description}'
    await smtp_sender.send_message(subject=subject, content=content)


async def set_periodics(periodics: dict, smtp_sender, machine_name: str):
    for k, v in periodics.items():
        file, interval_str = v.split(' ')
        interval = int(interval_str)
        description = k
        per_job = PeriodicCalllback(interval=interval, coro=_send_file_content, file=file, smtp_sender=smtp_sender,
                                    machine_name=machine_name, description=description)
        await per_job.start(delay=0)
