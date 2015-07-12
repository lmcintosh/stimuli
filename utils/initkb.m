function ex = initkb(ex)
%
% FUNCTION ex = initkb(ex)
%
% Initialize the keyboard.
%
% (c) bnaecker@stanford.edu 2014 
% 21 Jan 2014 - wrote it

% Supress keystrokes in MATLAB command window
%ListenChar(2);

% Important keys
KbName('UnifyKeyNames');
key.esc   = KbName('ESCAPE');
key.space = KbName('space');
key.t     = KbName('t');

% Initialize KbCheck and return
[key.keydown, key.secs, key.keycode] = KbCheck(-1);
key.keydown = 0;
ex.key      = key;
