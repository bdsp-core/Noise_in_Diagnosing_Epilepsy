function fcnGaussianPlot(spNo,x,titleStr)

% fit gaussian to data
[m,s] = normfit(x); 
xx = linspace(-20,20,1000); 
y = normpdf(xx,m,s); y=y/max(y); 

subplot(7,3,spNo); 
plot(x,x*0-0.1,'k|')
hold on; 
fill([xx, fliplr(xx)], [zeros(size(xx)), fliplr(y)], [.8 .8 .8], 'EdgeColor', 'none');
plot(xx,y,'k','linewidth',2);


text_x = -14; % X-coordinate for the text
text_y = .7; % Y-coordinate for the text
text_str = sprintf('\\sigma = %.1f', s); % Format the text string
text(text_x, text_y, text_str, 'FontSize', 14); % Add the text to the plot

set(gca,'XTick','');
set(gca,'YTick','');
axis off

box off
title(titleStr)
xlim([-15 15])