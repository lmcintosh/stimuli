function ex = initexptstruct()
%
% FUNCTION ex = initexptstruct()
%
% Initialize a structure to hold all experimental information
%
% (c) bnaecker@stanford.edu 2014 
% 22 Jan 2014 - wrote it

% experiment fields
ex = struct('stim', {[]}, 'disp', {[]}, 'key', {[]}, 'me', {[]});

% store the date
ex.today = datestr(now, 'yy-mm-dd');
