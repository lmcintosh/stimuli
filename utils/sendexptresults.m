function ex = sendexptresults(ex)
%
% FUNCTION ex = sendexptresults(ex)
%
% Print the results, either succes or failure, to the screen. Also, 
% notify via Pushover.
%
% (c) bnaecker@stanford.edu 2013 
% 30 Jan 2014 - updating for simple branch

% Check if there was an error of some kind
if isa(ex.me, 'MException')

  if strncmp(ex.me.identifier, 'checkesc', 8)
    statusStr = 'aborted';
  else
    statusStr = 'failed';
  end

  saveStr = sprintf('in workspace');
  errStr = sprintf('%s', ex.me.message);
  flipStr = '';

else

  statusStr = sprintf('success');
  saveStr = sprintf('saved data in %s', fullfile('/', ex.today, '/expt.json'));
  errStr = sprintf('no errors');

  % Check if flips were missed
  tol = 1e-3; % tolerance in seconds
  flipStr = '';
  for stimidx = 1:length(ex.stim)
      
      frametime = 1 / ex.stim{stimidx}.framerate;
      mu = mean(abs(diff(ex.stim{stimidx}.timestamps) - frametime) > tol);
      
      if mu > 0
          flipStr = [flipStr, '\n', ...
                     sprintf('(%i) %s\t\t%2.2f%% of flips were missed.', ...
                              stimidx, ex.stim{stimidx}.function, mu)];
      else
          flipStr = [flipStr, '\n', ...
                     sprintf('(%i) %s\t\tNo flips missed.', ...
                              stimidx, ex.stim{stimidx}.function)];
      end
  end

end

% Make the notification string
expStr = sprintf(['\n' ...
		 'date:\t\t%s\n' ...
		 'status:\t\t%s\n' ...
		 'save:\t\t%s\n' ...
		 'error:\t\t%s\n' ...
		 '%s'], ...
		 datestr(now), statusStr, saveStr, errStr, sprintf(flipStr));

% Print to the screen
fprintf(expStr);

% Notify via pushover, only if experiment not quit early
if ~(isa(ex.me, 'MException') && strcmp(ex.me.identifier, 'checkesc:escpressed'))
  send('Experiment results', expStr);
end
