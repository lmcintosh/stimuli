% Main psychToolbox experiment control script
%
% manages stimulus generation and metadata for Baccus lab experiments
%
% (c) 2015 Niru Maheswaranathan
% 
%   based off of Ben Naecker's setup:
%   https://github.com/bnaecker/basic-stimulus
%
% 28 Apr 2015 - initial version
addpath('jsonlab/')
addpath('utils/')
addpath('functions/')

% turn the `debug` flag on when testing
debug = true;

try

  % Construct an experimental structure array
  ex = initexptstruct();

  % Initialize the keyboard
  ex = initkb(ex);

  % Initalize the visual display
  ex.disp.bgcol = 0;
  ex = initdisp(ex);

  % wait for trigger
  ex = waitForTrigger(ex);

  % Parse this day's experiment config file
  basedir = fullfile('logs/', ex.today);
  stimuli = loadjson(fullfile(basedir, 'config.json'));

  % Run the stimuli
  for stimidx = 1:length(stimuli)

    % get the function name for this stimulus
    ex.stim{stimidx}.function = stimuli{stimidx}.function;

    % get the user-specified parameters
    ex.stim{stimidx}.params = rmfield(stimuli{stimidx}, 'function');
    
    % run this stimulus
    eval(['ex = ' ex.stim{stimidx}.function '(ex, false);']);

  end

  % Check for ESC keypress during the experiment
  ex = checkesc(ex);

  % Close windows and textures, clean up
  endexpt();

  if ~debug

    % Save the experimental metadata
    savejson('', ex, fullfile(basedir, 'expt.json'));

    % Send results via Pushover
    sendexptresults(ex);
    
    % commit and push
    commitStr = sprintf(':checkered_flag: Finished experiment on %s', datestr(now));
    evalc(['!git add .; git commit -am "' commitStr '"; git push;']);
    
  end

% catch errors
catch me

  % store the error
  ex.me = me;
  disp(ex.me);

  % Close windows and textures, clean up
  endexpt();

  % Send results via Pushover
  if ~debug
    sendexptresults(ex);
  end

end
