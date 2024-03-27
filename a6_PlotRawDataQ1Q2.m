clear all; clc; format compact; 

load Data; % T1, T2, T3, difficulty (1-4)

names = T1(:,1); 
y = T1(:,2); 
q11 = table2array(T1(:,4:3:end));
q21 = table2array(T1(:,5:3:end)); 
q12 = table2array(T2(:,2:3:end));
q22 = table2array(T2(:,3:3:end)); 

%% MAKE PLOTS FOR Q1

% raw answers [Question, Occasion]
y11 = ones(size(q11))*0.5;   y11(q11==1) = 1; y11(q11==3)=0; 
y12 = ones(size(q11))*0.5;   y12(q12==1) = 1; y12(q12==3)=0; 

load BestZ % z c l p y mn

[~,jj] = sort(c); c=c(jj); 
[~,ii] = sort(l); l=l(ii); 

y21 = zeros(size(q11));   y21(q21==1|y11==1) = 1;
y22 = zeros(size(q11));   y22(q22==1|y12==1) = 1; 

d1 = y11~=y12;  
d2 = y21~=y22;

L = l*ones(1,50);
C = ones(20,1)*c; 
PN = p;

% Data to be plotted
data = {y11(ii,jj), y21(ii,jj), y12(ii,jj), y22(ii,jj), d1(ii,jj), d2(ii,jj)};

% Loop through each data set and create individual plots
for i = 1:6
    fig = figure;
    set(fig, 'Units', 'inches', 'Position', [1, 1, 5, 2]);
    ax = axes(fig);
    imagesc(ax, data{i}, [0 1]);
    
    % Add labels on specific plots
    if i == 4 % Adjust based on your condition
        xlabel('Cases');
        ylabel('Experts');
    end
    
    axis off; % Hide axes
    colormap(ax, gray); % Set colormap to gray
    daspect(ax, [2 5 1]); % Adjust data aspect ratio to 2:5

    % Remove the white space and make the background transparent
    exportgraphics(ax, sprintf('plot_%d_Q2.png', i), 'Resolution', 300, 'BackgroundColor','none', 'ContentType','image');
    close(fig);
end

colormap gray