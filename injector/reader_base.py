class ReaderBase:
    # 属性：excluded_sigs、inputs_only、replay_blocks、signal_values、signal_changes
    def __init__(self, replay_blocks, wave_file, excluded_sigs, inputs_only):     
        self.excluded_sigs = excluded_sigs if excluded_sigs != None else []     # 信号集合
        self.inputs_only = inputs_only if inputs_only != None else True

        if type(replay_blocks) != list:
            replay_blocks = [replay_blocks]
        self.replay_blocks = replay_blocks

        # 从波形中读取数据，得到字典{'信号':[(时间,'值'),...],...}
        self.signal_values = self.extract_values_from_wave(self.replay_blocks, self.excluded_sigs, inputs_only)

        # 从signal_values中提取所有信号发生变化的时间，得到列表
        self.signal_changes = self.extract_events(self.signal_values)

        self.signal_values_i = {}
        self.signal_values_o = {}
        self.countIO()

    def countIO(self):
        for key in self.signal_values:
            if key.endswith('_i'):
                self.signal_values_i[key] = self.signal_values[key]
            else:
                self.signal_values_o[key] = self.signal_values[key]
        if self.inputs_only is True:
            self.signal_values = self.signal_values_i

    # 从波形中读取数据，得到字典{'信号':[(时间,'值'),...],...}
    def extract_values_from_wave(self, replay_blocks, excluded_sigs, inputs_only):
    	pass
    
    # 从signal_values中提取所有信号发生变化的时间，得到列表
    def extract_events(self, signal_values):
        all_changes = []

        for sig_name, sig_values in signal_values.items():
            all_changes.extend(sig_values)
        # 保留所有信号变化的时间
        change_times = sorted(list(set([change[0] for change in all_changes])))

        return change_times

    # 得到仿真时刻sim_time后的一个变化时刻，若无则返回None
    def get_next_event(self, sim_time):
        next_time = next((change_time for change_time in self.signal_changes if change_time > sim_time), None)
        return next_time

    # 返回字典--存放仿真时刻sim_time时各信号量的值
    def get_values_at(self, sim_time):
        current_values = {}
        for sig_name, sig_values in self.signal_values.items():
            # [::-1]表示倒序, next()返回迭代器的下一个项目
            # 返回字典--存放仿真时刻sim_time时各信号量的值
            current_values[sig_name] = next((sig_value[1] for sig_value in sig_values[::-1] if sig_value[0] <= sim_time), None)

        return current_values