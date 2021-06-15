import numpy as np

def convert_time_to_frame(timestamps: str, fps):
    # "00:10,00:13\n00:21,00:26\n..."
    frame_list = [[int(ts)*fps for ts in section.split(',')]
                  for section in timestamps.split("\n")]
    return frame_list

def convert_frames_to_summary(frames, total_frames):
    # [[240, 312], [504, 624], [720, 840], [1560, 1680], [2400, 2520],...]
    summary = np.zeros(total_frames, dtype="int")
    for section in frames:
        summary[section[0]-1:section[1]] = 1
    return summary

def convert_summary_to_time(frames, fps):
    # [0,0,0,0,1,1,1,1,.....0,0,0,0]
    ts_list = []
    start_ts = []
    end_ts = []
    for index, value in enumerate(frames):
        if value == 1:
            if (frames[index-1] == 0 and frames[index] == 1):
                start_ts.append(int((index+1)/fps))
            elif (frames[index] == 1 and frames[index+1] == 0):
                end_ts.append(int((index+1)/fps))

    ts_list = [[start, end] for start, end in zip(start_ts, end_ts)]
    return ts_list

