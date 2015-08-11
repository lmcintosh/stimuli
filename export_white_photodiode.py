import numpy as np
import os
import binary
import string

# This script finds the times of each white frame
# appearing in the photodiode channel.

# where are the experiment's bin files?
data_dir = os.path.expanduser('~/Documents/Stanford/00 Baccus Lab/Data 2015_07_02/')
experiment_date = '150702'
white_threshold = -4.75
num_bin_files = 14
bin_file_suffices = string.ascii_lowercase[:num_bin_files]
fs = 10000.0 # Hz
#bin_file_duration = 1000.0 # seconds

# store timestamps of each white frame
white_frame_timestamps = []
cumulative_total_samples = 0

# for each bin file
for idl, letter in enumerate(bin_file_suffices):
    # load bin files
    bin_filename = '%s%s.bin' %(experiment_date, letter)
    bin_file = data_dir + bin_filename
    raw_data = binary.readbin(bin_file)[:,0] #, chanlist=[0])
    
    # Get snippets of local maxima that cross white_threshold
    indices_passing_thresh = np.argwhere(raw_data > white_threshold)[:,0]
    if len(indices_passing_thresh) > 0:
        start_of_white_frame = [indices_passing_thresh[0]]
        end_of_white_frame = []
        for idd, d in enumerate(np.diff(indices_passing_thresh)):
            if d > 1:
                start_of_white_frame.append(indices_passing_thresh[idd+1])
                end_of_white_frame.append(indices_passing_thresh[idd])
        end_of_white_frame.append(indices_passing_thresh[-1])
        if len(start_of_white_frame) != len(end_of_white_frame):
            raise Exception('Have %d starts but %d ends to local maxima.' \
                    %(len(start_of_white_frame), len(end_of_white_frame)))

        for start, end in zip(start_of_white_frame, end_of_white_frame):
            if end - start == 0:
                peak = start
            else:
                snippet = raw_data[start:end]
                try:
                    peak = start + np.argmax(snippet)
                except:
                    import pdb
                    pdb.set_trace()
            # append time in current file + time that was in previous bin files
            #print (letter, (peak/fs + idl*bin_file_duration)/60., (peak/fs + idl*bin_file_duration)/3600.)
            #fig = plt.gcf()
            #ax = plot(raw_data[start-10000:start+10000])
            #plt.show()
            #time.sleep(2)
        
            white_frame_timestamps.append((peak + cumulative_total_samples)/fs)
    cumulative_total_samples += len(raw_data)

save_filename = data_dir + 'photodiode_white_frame_timestamps.txt'
np.savetxt(save_filename, white_frame_timestamps, fmt='%10.6f')
