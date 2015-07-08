function endexpt()
%
% FUNCTION endexpt()
%
% Closes all windows and textures, and returns cursors and keyboard control
% to the user.
%
% (c) bnaecker@stanford.edu 2014 
% 21 Jan 2014 - wrote it

Screen('CloseAll');
ListenChar(0);
ShowCursor;
Priority(0);
