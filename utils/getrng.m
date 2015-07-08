function s = getrng(seed)
%
% FUNCTION s = getrng(seed)
%
% Creates the standard random number generator used to generate random values for
% all experiments in the Baccus lab.
%
% (c) bnaecker@stanford.edu 2014 

if nargin == 0
  seed = 0;
end
s = RandStream('mt19937ar', 'Seed', seed);
