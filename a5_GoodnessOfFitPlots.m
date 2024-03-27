clear all; clc; format compact


%% show comparisons of l ~ li, c ~cj, p ~pij
figure(5); clf; 

load Data; % T1, T2, T3, difficulty (1-4)
names = T1(:,1); 
ind = find(difficulty>0); 
[y11,y12,y21,y22] = fcnGetData(T1,T2,ind);

%-----------------------------
% QUESTION 1
%-----------------------------
load BestZ % z c l p y mn
[Pr,li,l1,cj,c1,pij,P1] = fcnSetupForGooodnessOfFitPlots(y11,y12,c,l,p,y,sig);
sp = [1 3 5];
fcnPlotGoF(sp,Pr,li,l1,cj,c1,pij,P1);

%-----------------------------
% QUESTION 2
%-----------------------------
load BestZ2 % z c l p y mn
[Pr,li,l1,cj,c1,pij,P1] = fcnSetupForGooodnessOfFitPlots(y21,y22,c,l,p,y,sig);
sp = [2 4 6];
fcnPlotGoF(sp,Pr,li,l1,cj,c1,pij,P1);