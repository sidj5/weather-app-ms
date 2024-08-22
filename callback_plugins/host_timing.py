from ansible.plugins.callback import CallbackBase
import time

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'host_timing'

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__(*args, **kwargs)
        self.host_times = {}

    def v2_playbook_on_start(self, playbook):
        self.start_time = time.time()

    def v2_playbook_on_play_start(self, play):
        # Initialize host timing at the start of the play
        for host in play.get_variable_manager()._inventory.get_hosts():
            self.host_times[host.get_name()] = time.time()

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        if host not in self.host_times:
            self.host_times[host] = time.time()

    def v2_playbook_on_stats(self, stats):
        total_time = time.time() - self.start_time
        self._display.banner("HOST-LEVEL TIMING")
        for host, start_time in self.host_times.items():
            elapsed_time = time.time() - start_time
            self._display.display(f"Host {host} took {elapsed_time:.2f} seconds to execute the playbook")
        self._display.display(f"Total playbook execution time: {total_time:.2f} seconds")
