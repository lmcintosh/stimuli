function ex = checkkb(ex)
%
% FUNCTION ex = checkkb(ex)
%
% Checks the keyboard for keypresses
%
% (c) bnaecker@stanford.edu 2014 
% 21 Jan 2014 - wrote it
% 30 Jan 2014 - updating to collect everything in ex

[ex.key.keydown, ex.key.secs, ex.key.keycode] = KbCheck(-1);
