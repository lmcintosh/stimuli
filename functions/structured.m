function ex = structured(ex, replay)
%
% ex = structured(ex, replay)
%
% Required parameters:
%   length : float (length of the experiment in minutes)
%   framerate : float (rough framerate, in Hz)
%   structdir: string (location of the movies)
%   structext: string (file extension for the movies)
%
% Optional parameters:
%   seed : int (for the random number generator. Default: 0)
%
% Runs a natural movie from specified natural_movie_frames.mat file

  if replay

    % load experiment properties
    numframes = ex.numframes;
    me = ex.params;

    % set the random seed
    rs = getrng(me.seed);
    
    % all the saved structured stimuli are 50 x 50
    me.ndims = [50, 50];

  else

    % shorthand for parameters
    me = ex.stim{end}.params;

    % initialize the VBL timestamp
    vbl = GetSecs();

    % initialize random seed
    if isfield(me, 'seed')
      rs = getrng(me.seed);
    else
      rs = getrng();
    end
    ex.stim{end}.seed = rs.Seed;

    % compute flip times from the desired frame rate and length
    if me.framerate > ex.disp.frate
        error('Your monitor does not support a frame rate higher than %i Hz', ex.disp.frate);
    end
    flipsPerFrame = round(ex.disp.frate / me.framerate);
    ex.stim{end}.framerate = 1 / (flipsPerFrame * ex.disp.ifi);
    flipint = ex.disp.ifi * (flipsPerFrame - 0.25);

    % darken the photodiode
    Screen('FillOval', ex.disp.winptr, 0, ex.disp.pdrect);
    vbl = Screen('Flip', ex.disp.winptr, vbl + flipint);

    % store the number of frames
    numframes = ceil((me.length * 60) * ex.stim{end}.framerate);
    ex.stim{end}.numframes = numframes;
    
    % store timestamps
    ex.stim{end}.timestamps = zeros(ex.stim{end}.numframes,1);

  end


  % load natural movie frames
  files = dir(fullfile(me.structdir, me.structext));
  numstim = length(files);
  movies = cell(numstim, 1);
  for fileidx = 1:numstim
    movies(fileidx) = struct2cell(load(fullfile(me.structdir, files(fileidx).name)));
  end
  
  % flag to tell us if we should start a new structured stimulus
  start_new_seq = true;
  start_new_struct = true;

  % loop over frames
  for fi = 1:numframes

    if start_new_seq
      this_ordering = randperm(rs, numstim);
      progress_in_seq = 1;
      start_new_seq = false;
    end
      
    % pick a new stimulus
    if start_new_struct

      mov = movies{this_ordering(progress_in_seq)};
      
      % start at first frame
      current_frame = 1;
      start_new_struct = false;

      % keep one movie frame
      img = squeeze(mov(current_frame,:,:));

      % increase frame by one
      current_frame = current_frame + 1;

    % jitter
    else

      % keep one movie frame
      img = squeeze(mov(current_frame,:,:));

      % increase frame by one
      current_frame = current_frame + 1;

      % check if on last frame
      if current_frame >= size(mov,1)
        start_new_struct = true;
        progress_in_seq = progress_in_seq + 1;
      end

      % check if on last stimuli in sequence
      if progress_in_seq >= numstim
        start_new_seq = true;
      end

    end

    % get the new frame
    % assumes frame is already uint8, scaled between 0 and 255!!!
    % assumes frame is also already the correct size!
    frame = img * me.contrast + (1 - me.contrast) * ex.disp.gray;

    if replay

      % write the frame to the hdf5 file
      h5write(ex.filename, [ex.group '/stim'], uint8(frame), [1, 1, fi], [me.ndims, 1]);

    else

      % make the texture
      texid = Screen('MakeTexture', ex.disp.winptr, frame);

      % draw the texture, then kill it
      Screen('DrawTexture', ex.disp.winptr, texid, [], ex.disp.dstrect, 0, 0);
      Screen('Close', texid);

      % update the photodiode with the top left pixel on the first frame
      if fi == 1
        pd = ex.disp.white;
      elseif start_new_struct
        pd = 0.8 * ex.disp.white;
      else
        pd = ex.disp.pdscale * frame(1);
      end
      Screen('FillOval', ex.disp.winptr, pd, ex.disp.pdrect);

      % flip onto the scren
      Screen('DrawingFinished', ex.disp.winptr);
      vbl = Screen('Flip', ex.disp.winptr, vbl + flipint);

      % save the timestamp
      ex.stim{end}.timestamps(fi) = vbl;

      % check for ESC
      ex = checkkb(ex);
      if ex.key.keycode(ex.key.esc)
        fprintf('ESC pressed. Quitting.')
        break;
      end

    end

  end

end
