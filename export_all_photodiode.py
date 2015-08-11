import numpy as np
import os
import binary
import string
import h5py

# This script finds the times of each all frame
# appearing in the photodiode channel.

# where are the experiment's bin files?
data_dir = os.path.expanduser('~/Documents/Stanford/00 Baccus Lab/Data 2015_07_02/')
experiment_date = '150702'
all_threshold = -4.91
num_bin_files = 14
bin_file_suffices = string.ascii_lowercase[:num_bin_files]
fs = 10000.0 # Hz
#bin_file_duration = 1000.0 # seconds

# store timestamps of each all frame
all_frame_timestamps = []
all_frame_inds = []
all_frame_values = []
which_bin_file = []
cumulative_total_samples = 0

# for each bin file
for idl, letter in enumerate(bin_file_suffices):
    # load bin files
    bin_filename = '%s%s.bin' %(experiment_date, letter)
    bin_file = data_dir + bin_filename
    raw_data = binary.readbin(bin_file)[:,0] #, chanlist=[0])
    
    # Get snippets of local maxima that cross all_threshold
    indices_passing_thresh = np.argwhere(raw_data > all_threshold)[:,0]
    if len(indices_passing_thresh) > 0:
        start_of_all_frame = [indices_passing_thresh[0]]
        end_of_all_frame = []
        for idd, d in enumerate(np.diff(indices_passing_thresh)):
            if d > 1:
                start_of_all_frame.append(indices_passing_thresh[idd+1])
                end_of_all_frame.append(indices_passing_thresh[idd])
        end_of_all_frame.append(indices_passing_thresh[-1])
        if len(start_of_all_frame) != len(end_of_all_frame):
            raise Exception('Have %d starts but %d ends to local maxima.' \
                    %(len(start_of_all_frame), len(end_of_all_frame)))

        for start, end in zip(start_of_all_frame, end_of_all_frame):
            if end - start == 0:
                peak_ind = start
            else:
                snippet = raw_data[start:end]
                try:
                    peak_ind = start + np.argmax(snippet)
                except:
                    import pdb
                    pdb.set_trace()
        
            all_frame_timestamps.append((peak_ind + cumulative_total_samples)/fs)
            all_frame_inds.append(peak_ind)
            all_frame_values.append(raw_data[peak_ind])
            which_bin_file.append(letter)
    cumulative_total_samples += len(raw_data)


save_filename = data_dir + '%s_photodiode_all_frames_subsampled.hdf5' %(experiment_date)
f = h5py.File(save_filename, "w")
f['timestamps'] = all_frame_timestamps
f['indices'] = all_frame_inds
f['values'] = all_frame_values
f['file_index'] = which_bin_file
f.close()
