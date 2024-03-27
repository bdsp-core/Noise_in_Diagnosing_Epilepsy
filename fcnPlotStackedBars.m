function fcnPlotStackedBars(c,l,p,sig)

S = std(c); LN = std(l); PN = std(p(:)); ON = sig; 
n = [S LN PN ON];
n=n/sum(n)*100; 
y = n; 
cc = [0 0 0; 
    .4 0.4 0.4; 
    .5 0.5 0.5; 
    .6 .6 .6];

b = bar(0,y,"stacked");
xticklabels({''});

% Loop through each patch object and set its FaceColor
% Set colors for each segment
for i = 1:length(b)
    set(b(i), 'FaceColor', cc(i,:)); % Remove edge color
end

xticklabels({'Percentage'});

box off
set(gcf,'color','w')
axis off

% Starting position for the first text label
prevHeight = 0;
cumulativeSums = cumsum(y);
L = {'CV','LN','PN','ON'};
for i = 1:length(y)
    textPosition = (prevHeight + cumulativeSums(i)) / 2;
    str = [L{i} ': ' sprintf('%.0f%%', y(i))];
    text(0, textPosition, str, ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'middle', ...
        'Color', [1 1 1], 'FontSize', 14);
    prevHeight = cumulativeSums(i);
end

xlim([-.5 .5]); % Adjust x-axis limits to fit the bar
ylim([0 100]); % Adjust y-axis limits if needed
axis off
set(gca,'xtick',[])
set(gcf,'InvertHardCopy','off','Color','white');
b(1).BaseLine.Visible = 'off';
