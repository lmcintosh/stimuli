function fullpath = expanduser(str)
%
% FUNCTION fullpath = expanduser(str)
%
% Utility to expand the home directory (`~`) in path strings
%
% (c) nirum@stanford.edu 2015
% 28 Apr 2015 - wrote it

  % ensure the tilde shows up first
  if ~strcmp(str(1), '~')
    error('The input string must start with: ~');
  end

  % get home directory
  if ispc
    homedir = [getenv('HOMEDRIVE') getenv('HOMEPATH')];
  else
    homedir = getenv('HOME');
  end

  fullpath = fullfile(homedir, str(2:end));

end
