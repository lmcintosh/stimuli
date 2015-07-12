function ex = waitForTrigger(ex)
%
% FUNCTION ex = waitForTrigger(ex)
%
% The function waitForTrigger deals with the various experiment trigger types.
% It pauses execution of the stimulus, requests that the experimenter press
% the spacebar to arm the trigger, and then either triggers on pressing the 't'
% key or uses WaitForRec, depending on the request.
%
% (c) bnaecker@stanford.edu 24 Jan 2013 

%% arm the trigger
Screen('DrawText', ex.disp.winptr, 'Press spacebar to arm trigger ... ', ...
	50, 50);
Screen('Flip', ex.disp.winptr);
while ~ex.key.keycode(ex.key.space) && ~ex.key.keycode(ex.key.esc)
	ex = checkkb(ex);
end

%% wait for trigger
if any(strcmp('m', {'m', 'manual'}))
	Screen('DrawText', ex.disp.winptr, 'Waiting for experimenter trigger (t) ... ', ...
		50, 50);
	Screen('FillOval', ex.disp.winptr, ex.disp.black, ex.disp.pdrect);
	Screen('Flip', ex.disp.winptr);
	while ~ex.key.keycode(ex.key.t)
		ex = checkkb(ex);
	end
else
	Screen('DrawText', ex.disp.winptr, 'Waiting for recording computer ... ', ...
		50, 50);
	Screen('FillOval', ex.disp.winptr, ex.disp.black, ex.disp.pdrect);
	Screen('Flip', ex.disp.winptr);
	WaitForRec;
	WaitSecs(0.5);
end

%% hide the cursor to start the experiment
HideCursor;
