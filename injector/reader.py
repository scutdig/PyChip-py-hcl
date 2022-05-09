
# 读波形
from injector.vcd_reader import VcdReader


def read_wave(wavefile, replay_block, inputs_only, excluded_sigs):
    # get file postfix check if supported   # 得到文件后缀查看是否支持
    
    wave_type = wavefile.split('.')[-1]     # 得到文件后缀（fsdb/vcd）

    supported_wave_formats = ['vcd', 'fsdb']

    if wave_type not in supported_wave_formats:     # 不属于fsdb和vcd文件，报错
        raise ValueError("Wavefile type: ", wave_type, " is currently not supported. Supported formats are: ", supported_wave_formats)

    data = None

    if wave_type == 'vcd':      # vcd文件
        # from waveRead.vcd_reader import VcdReader
        data = VcdReader(replay_block, wavefile, excluded_sigs, inputs_only)
    elif wave_type == 'fsdb':   # fsdb文件
        pass
        # from waveRead.fsdb_reader import FsdbReader
        # data = FsdbReader(replay_block, wavefile, excluded_sigs, inputs_only)

    return data     


if __name__ == '__main__':
    replay_block = []
    wavefile = "../simulation/wave.vcd"
    # wavefile = "./mcdt.vcd"
    excluded_sigs = []
    inputs_only = False
    data = read_wave(wavefile, replay_block, inputs_only, excluded_sigs)  # VcdReader对象
    print(data.sig_name_2_vcd_name)
    print(data.vcd_name_2_sig_name)
    print(data.signal_values)
