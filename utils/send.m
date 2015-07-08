% pushover notification script
% Niru Maheswaranathan
% Mon Aug 13 14:21:43 2012
% send(msgTitle, msgText)

function send(msgTitle, msgText)

    % check if msgText is a runtime
    if isa(msgText,'numeric')
        if msgText/60 < 1 % smaller than a minute
            msgText = sprintf('Took %5.3f seconds.',msgText);
        elseif msgText/3600 < 1 % smaller than an hour
            msgText = sprintf('Took %5.3f minutes.',msgText/60);
        else
            msgText = sprintf('Took %5.3f hours.',msgText/3600);
        end
    end

    userKey    = 'VnKXLJ5EfypjQb9GLRkRKV6z63daQf';
    appToken   = 'S6F9y5CccnW7wVqkUqb9sXrKAXe6uV';
    deviceName = 'phone';

    params = { ...
        'token',   appToken, ...
        'user',    userKey, ...
        'device',  deviceName, ...
        'title',   msgTitle, ...
        'message', msgText};

    url = 'https://api.pushover.net/1/messages.json';

    s = urlread(url,'POST',params);
