import os
import random
import threading
import time
from multiprocessing import Manager, Process, Queue
from multiprocessing.managers import SyncManager
from typing import Any, Callable, Dict, List, Union

# 引擎正在运行中。有任务在运行
SIG_ACTI = 40
# 引擎正在休眠中。任务等待区无任务，且无运行中任务
SIG_SLEP = 30
# 状态分界线。大于0说明系统正常运行中；小于0说明系统需要即将关闭或立刻关闭，不再将等待区的任务加入多线程中运行
SIG_LINE = 0
# 列表中任务执行完成。且等待区无新任务，由 __thread_active_tasks_waiting 函数通知引擎关闭
SIG_FINI = -10
# 要求引擎停止。不再追加任务，等待正在运行的进程结束后停止引擎
SIG_STOP = -20
# 要求引擎终止。立刻终止所有线程、进程，所有执行中的进程将终止
SIG_TMNT = -30

KEY_STATUS = 'CURRENT_STATUS'


class AutoProcess:
    auto_end: Union[bool, int]
    auto_end_wait_time: int
    auto_end_last_time: int
    tasks_waiting: List[Process]
    tasks_running: List[Process]
    tasks_finish_number: int
    signal: int
    number: int
    __thread_active_tasks_waiting: threading.Thread
    __thread_clear_tasks_complate: threading.Thread
    activated_or_not: bool
    scan_interval: float
    __queue: SyncManager.Queue
    TASK_KEY: str

    def __init__(self,
                 number: int = 8,
                 auto_end: Union[bool, int] = 3,
                 scan_interval: float = 1,
                 queue: SyncManager.Queue = None) -> None:
        '''
        同步函数，等待任务执行结束退出
        number: 最大运行进程数量，该值小于0时，只要任务等待区有任务就会无限塞入任务运行区运行
        auto_end: 任务运行完后是否自动结束
        scan_interval: 扫描间隔，不建议低于1，否则线程太过占用系统资源，根据运行设备情况自定义
        '''
        self.auto_end = auto_end
        self.auto_end_last_time = time.time()
        if isinstance(auto_end, int):
            self.auto_end_wait_time = auto_end
        else:
            self.auto_end_wait_time = 30
        self.tasks_waiting = []
        self.tasks_running = []
        self.signal = SIG_SLEP
        self.number = number
        self.is_activated = False
        self.scan_interval = scan_interval
        self.tasks_finish_number = 0
        if queue:
            self.__queue = queue
        else:
            manager = Manager()
            self.__queue = manager.Queue()
        self.TASK_KEY = 'TASKID'
        self.RET_KEY = 'RETURNDATA'

    def __active_tasks_waiting(self):
        '''
        将任务等待区中的任务放入多线程运行，定期扫描等待区任务
        scan_interval: 扫描间隔
        '''
        while True:
            if self.signal < SIG_LINE:
                return
            if self.auto_end and time.time() - (
                    self.auto_end_last_time +
                    self.auto_end_wait_time) > 0 and len(
                        self.tasks_waiting) == 0 and len(
                            self.tasks_running) == 0 and self.is_activated:
                # 在自动关闭开关激活，超过自动等待时间，且等待区没有任务，且本函数已经激活过。发出任务运行完成，发出任务完成信息，退出引擎
                self.signal = SIG_FINI
                return
            for i in range(len(self.tasks_waiting)):
                if self.number > 0 and len(self.tasks_running) >= self.number:
                    break
                process = self.tasks_waiting.pop(0)
                process.start()
                self.tasks_running.append(process)
                self.is_activated = True
                self.signal = SIG_ACTI
            if len(self.tasks_waiting) == 0 and len(self.tasks_running) == 0:
                self.signal = SIG_SLEP
            # print('__active_tasks_waiting scanning...')
            # print('waiting tasks number:', len(self.tasks_waiting))
            # print('current state number:', self.signal)
            time.sleep(self.scan_interval)

    def __clear_tasks_complate(self):
        '''
        将任务运行区已完成的任务定期进行清理，定期扫描运行区任务
        scan_interval: 扫描间隔
        '''
        while True:
            for process in self.tasks_running:
                if self.signal == SIG_TMNT:
                    process.kill()
                    process.join()
                    process.close()
                elif not process.is_alive():
                    self.tasks_running.remove(process)
                    if hasattr(process, 'close'):
                        process.close()
                    self.auto_end_last_time = time.time()
                    self.tasks_finish_number += 1
            if self.signal == SIG_TMNT:
                return
            if self.signal < SIG_LINE and len(self.tasks_running) == 0:
                return
            # print('__clear_tasks_complate scanning...')
            # print('running tasks number:', len(self.tasks_running))
            # print('current state number:', self.signal)
            time.sleep(self.scan_interval)

    def get_return(self, queue: SyncManager.Queue = None):
        '''
        '''
        if queue:
            while not queue.empty():
                yield queue.get()
        while not self.__queue.empty():
            yield self.__queue.get()

    def gen_task_id(self) -> str:
        return os.urandom(16).hex()

    def put_task(self,
                 func: Callable,
                 args: List = None,
                 kwargs: Dict = None,
                 queue: Union[bool, SyncManager.Queue] = False) -> str:
        '''
        提交待执行的任务，返回任务id
        func: 要多进程运行的函数
        args: 任务函数的参数
        kwargs: 任务函数的kw参数
        '''
        if not args:
            args = []
        if not kwargs:
            kwargs = {}
        if queue and isinstance(queue, bool):
            args.insert(0, self.__queue)
        else:
            args.insert(0, queue)
        self.tasks_waiting.append(
            Process(target=func, args=args, kwargs=kwargs))

    def wait(self, timeout: Union[int, None] = None):
        '''
        同步函数，等待任务执行结束退出
        timeout: 超时结束
        '''
        self.__thread_active_tasks_waiting.join(timeout)
        self.__thread_clear_tasks_complate.join(timeout)

    def stop(self):
        '''
        向引擎发出停止信号
        '''
        self.signal = SIG_STOP

    def terminate(self):
        '''
        向引擎发出终止信号
        '''
        self.signal = SIG_TMNT

    def run(self):
        '''
        该函数会将输入的函数放入线程池中进行调度，调度会把任务放入子进程中进行运行
        scan_interval: 扫描间隔
        '''
        self.__thread_active_tasks_waiting = threading.Thread(
            target=self.__active_tasks_waiting)
        self.__thread_clear_tasks_complate = threading.Thread(
            target=self.__clear_tasks_complate)
        self.__thread_active_tasks_waiting.start()
        self.__thread_clear_tasks_complate.start()


def test_performance_func(min: int, max: int):
    # print(os.getpid(), 'test_normal_func running...')
    result = 0
    for i in range(random.randint(min, max)):
        for j in range(random.randint(min, max)):
            for k in range(random.randint(min, max)):
                result += i * j * k
    print(os.getpid(), 'test_normal_func result:', str(result))
    # print(os.getpid(), 'test_normal_func ending...')


def test_normal_func(min: int, max: int):
    # print(os.getpid(), 'test_normal_func running...')
    if random.randint(0, 1):
        # 模仿部分进程执行较快，部分进程执行较慢
        result = 0
        for i in range(random.randint(min, max)):
            for j in range(random.randint(min, max)):
                for k in range(random.randint(min, max)):
                    result += i * j * k
        print(os.getpid(), 'test_normal_func result:', str(result))
    # print(os.getpid(), 'test_normal_func ending...')


def test_return_func(queue: Queue, min: int, max: int):
    result = 0
    for i in range(random.randint(min, max)):
        for j in range(random.randint(min, max)):
            for k in range(random.randint(min, max)):
                result += i * j * k
    # 返回数据
    queue.put(result)
    print(os.getpid(), 'test_return_func result:', str(result))


if __name__ == '__main__':
    '''
    多进程使用要求必须把代码放在 if __name__ == '__main__' 这部分下
    '''
    # ----------------功能测试部分----------------
    autopro = AutoProcess()
    autopro.run()

    # 返回值获取测试
    [
        autopro.put_task(test_return_func, [100, 999], queue=True)
        for i in range(8)
    ]
    autopro.wait()
    print('current state number:', autopro.signal)
    print('finish task number:', autopro.tasks_finish_number)
    returndata = [i for i in autopro.get_return()]
    print(len(returndata))
    print(returndata)

    # # 同步等待功能测试
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # autopro.wait()
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)

    # # 多次塞入任务测试
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(10)]
    # time.sleep(20)
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(10)]
    # time.sleep(20)
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(10)]
    # time.sleep(20)
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(10)]
    # autopro.wait()
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)

    # # 中途发出停止信号测试
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # time.sleep(10)
    # autopro.stop()
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # time.sleep(10)
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # autopro.wait()
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)

    # # 中途发出终止号测试
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # time.sleep(10)
    # autopro.terminate()
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # time.sleep(10)
    # [autopro.put_task(test_normal_func, (100, 999)) for i in range(20)]
    # autopro.wait()
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)

    # # ----------------性能测试部分----------------
    # # 性能测试，正常运行，100个任务，用于对比
    # start_time_1 = time.time()
    # [test_performance_func(500, 500) for i in range(100)]

    # # 性能测试，4进程，100个任务
    # autopro = AutoProcess(4)
    # autopro.run()
    # start_time_4 = time.time()
    # [autopro.put_task(test_performance_func, (500, 500)) for i in range(100)]
    # autopro.wait()

    # # 性能测试，20进程，100个任务
    # autopro = AutoProcess(20)
    # autopro.run()
    # start_time_20 = time.time()
    # [autopro.put_task(test_performance_func, (500, 500)) for i in range(100)]
    # autopro.wait()
    # print('1线程运行：')
    # print('total time(s):', time.time() - start_time_1)
    # print('4线程运行：')
    # print('total time(s):', time.time() - start_time_4)
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)
    # print('20线程运行：')
    # print('total time(s):', time.time() - start_time_20)
    # print('current state number:', autopro.signal)
    # print('finish task number:', autopro.tasks_finish_number)

    # # 1线程运行：
    # # total time(s): 1115.9921689033508
    # # 4线程运行：
    # # total time(s): 343.8757131099701
    # # current state number: -10
    # # finish task number: 100
    # # 20线程运行：
    # # total time(s): 350.890340089798
    # # current state number: -10
    # # finish task number: 100

    # # 测试平台：
    # # MacBook Pro (13-inch, 2020, Four Thunderbolt 3 ports)
    # # CPU：2 GHz 四核Intel Core i5
    # # 内存：16 GB 3733 MHz LPDDR4X
