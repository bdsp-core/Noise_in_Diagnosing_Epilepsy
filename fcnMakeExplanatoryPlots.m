function fcnMakeExplanatoryPlots(y11,y12,c,l,p,y,sig,q);


[~,jj] = sort(c); c=c(jj); 
[~,ii] = sort(l); l=l(ii); 

L = l*ones(1,50);
C = ones(20,1)*c; 
PN = p;

[ON1,ON2] = fcnGetOccasionNoiseSample(c,l,p,y,y11,y12,sig);

% plot results
x1 = C(:); 
x2 = L(:); 
x3 = ON1(:); 
x4 = ON2(:); 
x5 = PN(:); 
x = [x1; x2; x3; x4; x5];
mn = prctile(x,5);
mx = prctile(x,95);
clim = [mn mx];

SN1 = L+PN+ON1; 
SN2 = L+PN+ON2;
data = {C, L, PN, ON1, ON2, SN1, SN2};

% Find colorscale limits
x = [C(:); L(:); ON1(:); ON2(:); PN(:)];
mn = prctile(x,5);
mx = prctile(x,95);
clim = [mn mx];

% Loop through each data set and create individual plots
for i = 1:length(data)
    fig = figure;
    set(fig, 'Units', 'inches', 'Position', [1, 1, 5, 2]);
    ax = axes(fig);
    imagesc(ax, data{i});
    axis off; % Hide axes
    colormap(ax, gray); % Set colormap to gray
    daspect(ax, [2 5 1]); % Adjust data aspect ratio to 2:5

    % Remove the white space and make the background transparent
    exportgraphics(ax, sprintf('result_plot_%d_Q%d.png', i,q), 'Resolution', 300, 'BackgroundColor','none', 'ContentType','image');
    close(fig);
end

