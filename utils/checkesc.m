function ex = checkesc(ex)
%
% FUNCTION ex = checkesc(ex)
%
% Checks the keyboard information structure for escape keypresses. Used in
% quitting from experiments.
%
% (c) bnaecker@stanford.edu 2014 
% 22 Jan 2014 - wrote it
% 30 Jan 2014 - updating to collect everything in ex

%% Check
if ex.key.keycode(ex.key.esc)
	me = MException('checkesc:escpressed', ...
		['You quit the experiment early. Nothing will be saved, but the experimental ' ...
		'data structures are in your workspace']);
	throw(me);
end
