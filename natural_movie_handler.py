import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

class video_handler(object):
    '''
    Video handler obejct: an object designed to take raw .mp4 files
    of natural scenes, perform statistics on them and edit them
    
    
    Attributes
    ----------
    -self.clip: moviepy obj; 
    -self.metadata: dict; stores metadata about video
    -self.RMS: 1xn numpy array of 

    Methods
    ----------
    -__init__: constructor method for video_handler
    -set_metadata: setter used to update self.metadata dict
    
    v1.0: Jonathan Calles 1/30/17

    '''
    def __init__(self, filename = None, getRMS = False):
        '''
        Constructor method for video_handler. Allows for optional 
        implementation of load_video and getRMS with instantiation if flags 
        are set.
        
        
        Arguments
        ----------
        -filename: str; path to video file
        -getRMS: bool; flag for running getRMS on instantiation
        
        
        Returns
        ----------
        None
        
        
        '''
        self.metadata = {}# initialize metadata library
        self.RMS = None
        
        # optionally initialize with clip
        if filename:
            self.load_video(filename)
        else:
            self.clip = None
            
        # optionally run self.getRMS with default value if flagged
        if getRMS:
            self.getRMS()
            
        
        
    def set_metadata(self, prop, val):
        '''
        A method used to set metadata values for the video clip
        
        Arguments
        ----------
        -prop: str or list of str; key for metadata value
        -val: arbitrary/list of arbitrary types; value for metadata key
        
        Returns
        ----------
        None
        
        
        '''
        for i, key in enumerate(prop):
            self.metadata[key] = val[i]
        
    
    def load_video(self, filename):
        '''
        A method used to load an .mp4 file into the object for
        further processing. Also updates self.metadata to include
        the title, framerate and duration of the video.
        
        
        Arguments
        ----------
        -filename: str; path to video file in question
        
        Returns
        ----------
        None

        '''
        
        # load vile into object
        self.clip = VideoFileClip(filename, audio = False)
        
        # set framerate and video duration
        self.set_metadata(['title', 'framerate','duration'],
                          [filename, self.clip.fps, self.clip.duration])
        
        
    def getRMS(self, clip = None, t_start = 0, t_end = None, downsample = True,
               norm_flag = True, smooth = 15*60):
        '''
        A method to calculate the RMS between individual frames of a clip.
        Has optional parameters to set the start and end of RMS analysis.
        
        If the downsample flag is set, getRMS will only compare frames every
        second as opposed to at the framerate frequency
        
        If the norm_flag is set, getRMS will pass it to self.RMS() so that each
        frame is normalized by its mean luminance before calculating RMS.
        
        The smoothing parameter is used to specify whether or not to smooth the
        resulting RMS values with a step filter. The time duration of the 
        step filter should be specified in seconds (e.g. smoothing = 60 -->
        step filter of length 1 minute). Default smoothing is for 15 minutes
                                  
            
        Arguments
        ----------
        -clip: str; optional path to video file; use if video hasn't been
            loaded yet
        -t_start: float; optional start time for RMS analysis (in sec)
        -t_end: float; optional end time for RMS analysis (in sec), defaults
            to video end point
        -downsample: bool; flag telling getRMS whether or not to calculate RMS
            between every frame or just every second
        -norm_flag: bool; flag telling getRMS whether or not to normalize
            each frame by its luminance before calculating RMS
        -smooth: float; optional parameter telling getRMS whether or not to 
            smooth RMS with a step function of width 'smooth'. Set to None
            or False if no smoothing is desired
            
        
        Returns
        ----------
        None
    
        
        NOTE:In order to reduce memory footprint, individual video frames
        are only stored in a temporary variable while they are being used to
        calculate the RMS between it and the frame before and after it. To
        implement this, a 'toggle' variable is used so that the method 
        alternates saving frames between two elements of a list.
        
        
        NOTE: getRMS will update self.metadata with whether or not RMS was 
        calculated with or without normalization and downsampling.
        '''
        
        # set parameters if not specified
        if clip:
            self.load_video(clip)
        elif not self.clip:
            print('Error: No clip specified')
            return False

        # NOTE: if t_end is not specified, the method will run through
        #     throught the entire clip;
        if not t_end:
            if self.metadata['duration']:
                t_end = self.metadata['duration']
            else:
                print('Error: No endtime specified and clip duration \
                not defined in self.metadata')
                return False
            
        # define framerate and exit if not specified
        if self.metadata['framerate']:
            fps = self.metadata['framerate']
        else:
            print('Error: No framerate specified in metadata')
            return False
        
        
        # initialize toggle variable storage array
        toggle = 0
        frames = [ [], [] ]
        
        # calculate number of frames to analyze and allocate space for
        # temporary RMS variable
        num_frames = int(np.ceil((t_end - t_start)*fps))        
        RMS_array = np.zeros(num_frames)
        
        for i, frame in enumerate(self.clip.iter_frames()):
            # calculate time
            time = i/fps
            # is this frame within the time interval selected?
            if time < t_start:
                continue
            elif time > t_end:
                break
            
            # downsample if flag is set
            if downsample:
                # skip samples that don't fall on the exact second
                if not i % int(np.ceil(fps)) == 0:
                    continue
           
            # user feedback; print progress every n frames
            n = 200
            if i%n == 0:
                print('Processing Data: {0} s out of {1} s'.format(
                        time, t_end))
            # store frame in frames
            frames[toggle] = frame 
            # switch toggle value
            toggle = not toggle
            
            # ignore first iteration; continue if second element of 
            # frames is empty
            if frames[1] == []:
                continue
            else:
                RMS_array[i] = video_handler.RMS(frames[0], frames[1],
                         norm_flag = norm_flag)
                  
        # convolve data with step filter data if smoothing is set
        if smooth:
            # if downsample is set, the length of the step should be smooth
            #
            # if downsample is not set, the length of the step should be
            #     the duration of smooth times the framerate
            if not downsample:
                smooth *= fps
                
            step = np.ones(smooth*fps)
            RMS_array = np.convolve(RMS_array, step, mode='same')
            
        # set self.RMS
        self.RMS = RMS_array
        
        # update metadata to include whether or not RMS was downsampled or not
        self.set_metadata(['RMS Downsampled', 'RMS Normalized'],
                          [downsample, norm_flag])       
            
        
    @staticmethod
    def color2gray(R, G, B):
        '''
        A static method used to convert RGB to luminance
        for grayscale images
        
        
        Arguments
        ----------
        -R: float or list of floats; red channel
        -G: float or list of floats; green channel
        -B: float or list of floats; blue channel
        
        Returns
        ----------
        -luminance: float; luminance of pixel or array of pixels
        
        
        '''
        
        return (R+G+B)/3
    
    @staticmethod
    def RMS(x,y, norm_flag = False):
        '''
        A static method used to calculate the RMS between two 3 channel RGB
        frames x, y. Deliberately written such that x and y shape are
        unimportant as long as they match.
        
               
        Arguments
        ----------
        -x: HxWx3 np.array of uint8; first frame
        -y: HxWx3 np.array of uint8; second frame
        -norm_flag: bool; tells method whether or not to normalize luminance
            before calculating RMS
        
        Returns
        ----------
        - RMS: float; RMS of luminance between the two frames
        
        
        NOTE: converts 3 channels to luminance before calculating RMS
        '''
        # caluclate luminances of two frames
        xR, xG, xB = [x[:,:,i] for i in range(3)]
        xLum = video_handler.color2gray(xR, xG, xB)
        
        yR, yG, yB = [y[:,:,i] for i in range(3)]
        yLum = video_handler.color2gray(yR, yG, yB)
        
        # normalize each frame by mean luminance if norm_flag is set
        if norm_flag:
            xLum -= np.mean(xLum)
            yLum -= np.mean(yLum)
        
        # calculate RMS and return value
        return np.mean((xLum - yLum)**2)
    
    @staticmethod
    def peaks(array, numpeaks, spacing = None, sampling_rate = None,):
        '''
        A static method that takes an array of values and returns n peaks with
        their indices as well as time stamps. Optionally can select peaks with 
        a minimum spacing specified by the parameter "spacing".
        
        
        Arguments
        ----------
        -array: list or np.array; list of RMS values
        -numpeaks: int; number of desired peaks to return
        -sampling_rate: float or int; Optional; sampling rate of the array, or 
            how many indices per second
        -spacing: float or int; Optional; desired amount of time between peaks
            in seconds
        
        
        Returns
        ----------
        -peaks:dict; ['indices'] = 1xn np.array of the n largest peaks
                     ['sampling rate'] = float; frames per second
                     ['spacing'] = float; time length of bins in sec
        
        
        '''
        if type(array) == np.ndarray:
            pass
        else:
            try:
                array = np.array(array)
            except:
                return 'Error: array not castable to np.array'
    
        #if spacing and sampling rate:
        if sampling_rate and spacing:
            #calculate number of indices within spacing
            time_bins = sampling_rate*spacing
            #d_ind = divide by two to get plus/minus bound
            d_ind = time_bins/2
        else:
            d_ind = 0
        
        #declare indices array
        indices = np.zeros(numpeaks, dtype = np.uint64)
        
        # create np.array of data values and indices
        data = np.array([ 
                [i for i in range(len(array))], array ])
        
        # loop until the desired number of peaks are chosen
        for i in range(numpeaks):
            # get index at highest array value
            ind = np.argmax(data[1,:])
            #store these in indices
           # val = data[1,ind]
            indices[i] = data[0,ind]
            # remove peak and time bin surrounding it
            lbound = int(indices[i] - d_ind)
            ubound = int(indices[i] + d_ind)
            # declare list for data to del
            to_del = []
            for j in range(len(data[0,:])):
                if data[0,j] < lbound:
                    continue
                elif data[0,j] <= ubound:
                    to_del.append(j)
                else:
                    break
                
            # update data to ignore time bins
            data = data[:, 
                        [i for i in range(len(data[0,:])) if i not in to_del]]
    
        # return peaks dict
        peaks = {
            'indices' : indices,
            'sampling rate' : sampling_rate,
            'spacing' : spacing
        }
        
        return peaks
        
        
        
###############################################################################
#
#                                   TEST SCRIPT
#
###############################################################################
##%%
## instantiate video handler object
#animal = video_handler('test.mp4')
#animal.getRMS(smooth = 60, norm_flag = False)
#
#animalx = np.linspace(0,1,len(animal.RMS))*animal.metadata['duration']
#animaly1 = animal.RMS
#
#animal.getRMS(smooth = 60, norm_flag = True)
#animaly2 = animal.RMS
#
#okgo = video_handler('test2.mp4')
#okgo.getRMS(smooth = 60, norm_flag = False)
#
#okgox = np.linspace(0,1,len(okgo.RMS))*okgo.metadata['duration']
#okgoy1 = okgo.RMS
#
#
#okgo.getRMS(smooth = 60, norm_flag = True)
#okgoy2 = okgo.RMS
#
##%%
#f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
#ax1.plot(animalx, animaly1, '--r')
#ax2.plot(animalx, animaly2, '--r')
#ax3.plot(okgox, okgoy1, '--b')
#ax4.plot(okgox, okgoy2, '--b')
#
#plt.show()
#%%
# Test peaks finder
array = np.random.rand(1000)
peaks = video_handler.peaks(array, 5, 100, 1)