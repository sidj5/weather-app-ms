from ansible.plugins.callback import CallbackBase
import time

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'host_timing'

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self.host_start_times = {}
        self.host_end_times = {}

    def v2_playbook_on_start(self, playbook):
        pass  # No need to track the start of the entire playbook here

    def v2_playbook_on_play_start(self, play):
        for host in play.get_variable_manager()._inventory.get_hosts():
            self.host_start_times[host.get_name()] = None

    def v2_runner_on_start(self, host, task):
        if self.host_start_times[host.get_name()] is None:
            self.host_start_times[host.get_name()] = time.time()

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.host_end_times[host] = time.time()

    def v2_playbook_on_stats(self, stats):
        self._display.banner("HOST-LEVEL TIMING")
        for host, start_time in self.host_start_times.items():
            if start_time:
                elapsed_time = self.host_end_times[host] - start_time
                self._display.display(f"Host {host} took {elapsed_time:.2f} seconds to execute the playbook")
            else:
                self._display.display(f"Host {host} did not start any tasks")