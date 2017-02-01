import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

class video_handler(object):
    '''
    Video handler obejct: an object designed to take raw .mp4 files
    of natural scenes, perform statistics on them and edit them


    Note: definitely flesh this out later
    
    
    Attributes
    ----------
    

    Methods
    ----------

    '''
    
    #########################################################################
    ## Notes to Self
    ## -------------
    ## 
    ## - clip.iter_frames() iterates over every frame one at a time and
    ##       returns a HxWx(RGB) array of floats
    ##
    #########################################################################
    
    
    
    
    
    def __init__(self):
        self.meta = {}# initialize metadata library
        
        
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
        clip = VideoFileClip(filename, audio = False)
        
        # set framerate and video duration
        framerate = clip.fps
        duration = 
        self.set_metadata()

    
    def color2gray(self, R, G, B):
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
        @staticmethod
