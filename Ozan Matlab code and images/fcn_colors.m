function [colors,lines,markers] = fcn_colors()
% plotting color assignments

% Bright
colors.bright = cell(5*9);
for i = 1:5
    colors.bright{(i-1)*9+1} = 'k';
    colors.bright{(i-1)*9+2} = 'b';
    colors.bright{(i-1)*9+3} = 'r';
    colors.bright{(i-1)*9+4} = 'g';
    colors.bright{(i-1)*9+5} = 'c';
    colors.bright{(i-1)*9+6} = 'm';
    colors.bright{(i-1)*9+7} = 'y';
    colors.bright{(i-1)*9+8} = 'k';
    colors.bright{(i-1)*9+9} = 'w';
end

% matte
colors.matte = cell(5*7);
for i = 1:5
    colors.matte{(i-1)*7+1} = [0 0.4470 0.7410];      %blue
    colors.matte{(i-1)*7+2} = [0.8500 0.3250 0.0980]; %orange
    colors.matte{(i-1)*7+3} = [0.9290 0.6940 0.1250]; %yellow
    colors.matte{(i-1)*7+4} = [0.4660 0.6740 0.1880]; %green
    colors.matte{(i-1)*7+5} = [0.4940 0.1840 0.5560]; %purple
    colors.matte{(i-1)*7+6} = [0.3010 0.7450 0.9330]; %turquoise 
    colors.matte{(i-1)*7+7} = [0.6350 0.0780 0.1840]; %maroon
end


% lines
lines = cell(40);
for i = 1:10
    lines{(i-1)*4+1} = '-';
    lines{(i-1)*4+2} = '--';
    lines{(i-1)*4+3} = ':';
    lines{(i-1)*4+4} = '-.';
end


% markers
markers = cell(5*10);
for i = 1:5
    markers{(i-1)*10+1} = '.';
    markers{(i-1)*10+2} = 'o';
    markers{(i-1)*10+3} = '^';
    markers{(i-1)*10+4} = 's';
    markers{(i-1)*10+5} = 'd';
    markers{(i-1)*10+6} = '+';
    markers{(i-1)*10+7} = '*';
    markers{(i-1)*10+8} = 'x';
    markers{(i-1)*10+9} = 'v';
    markers{(i-1)*10+10} = '>';
end

end

