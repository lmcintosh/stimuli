import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

class video_handler(object):
    '''
    Video handler obejct: an object designed to take raw .mp4 files
    of natural scenes, perform statistics on them and edit them
    
    
    Attributes
    ----------
    -self.clip
    -self.metadata
    -self.RMS

    Methods
    ----------
    
    v1.0: Jonathan Calles 1/30/17

    '''
    
    #########################################################################
    ## Notes to Self
    ## -------------
    ## 
    ## - Flesh out the documentation of the individual sub methods
    ##
    ## - Flesh out the documentation for the class
    ##
    #########################################################################
    
      
    def __init__(self, filename = None, getRMS = False):
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
        '''
        for i, key in enumerate(prop):
            self.metadata[key] = val[i]
        
    
    def load_video(self, filename):
        '''
        A method used to load an .mp4 file into the object for
        further processing.

        '''
        
        # load vile into object
        self.clip = VideoFileClip(filename, audio = False)
        
        # set framerate and video duration
        self.set_metadata(['framerate','duration'],
                          [self.clip.fps, self.clip.duration])
        
        
    def getRMS(self, clip = None, t_start = 0, t_end = None, smooth = 15*60):
        '''
        A method to calculate the RMS between individual frames of a clip.
        Has optional parameters to set the start and end of RMS analysis. The
        smoothing parameter is used to specify whether or not to smooth the
        resulting RMS values with a step filter. The time duration of the 
        step filter should be specified in seconds (e.g. smoothing = 60 -->
        step filter of length 1 minute). Default smoothing is for 15 minutes
                                  
            
        Arguments
        ----------
        
        Returns
        ----------
        
        
        
        NOTE:In order to reduce memory footprint, individual video frames
        are only stored in a temporary variable while they are being used to
        calculate the RMS between it and the frame before and after it. To
        implement this, a 'toggle' variable is used so that the method 
        alternates saving frames between two elements of a list.
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
                RMS_array[i] = video_handler.RMS(frames[0], frames[1])
                  
        # convolve data with step filter data if smoothing is set
        if smooth:
            step = np.ones(smooth*fps)
            RMS_array = np.convolve(RMS_array, step, mode='same')
            
        # set self.RMS
        self.RMS = RMS_array
            
        
    @staticmethod
    def color2gray(R, G, B):
        '''
        A static method used to convert RGB to luminance
        for grayscale images
        
        
        Arguments
        ----------
        -R: float or array of floats; red channel
        -G: float or array of floats; green channel
        -B: float or array of floats; blue channel
        
        Returns
        ----------
        -luminance: float; luminance of pixel or array of pixels
        '''
        
        return (R+G+B)/3
    
    @staticmethod
    def RMS(x,y):
        '''
        A static method used to calculate the RMS between two 3 channel RGB
        frames x, y. Deliberately written such that x and y shape are
        unimportant as long as they match. .
        
               
        Arguments
        ----------
        -x: HxWx3 array of uint8; first frame
        -y: HxWx3 array of uint8; second frame
        
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
        
        # calculate RMS and return value
        return np.mean((xLum - yLum)**2)
    

###############################################################################
#
# TEST SCRIPT
#
###############################################################################

# instantiate video handler object
obj = video_handler('test.mp4', getRMS = True)
