clear all; clc; format compact; 

load Data; % T1, T2, T3, difficulty (1-4)

names = T1(:,1); 
y = T1(:,2); 
q11 = table2array(T1(:,4:3:end));
q21 = table2array(T1(:,5:3:end)); 
q12 = table2array(T2(:,2:3:end));
q22 = table2array(T2(:,3:3:end)); 

% raw answers [Question, Occasion]
y11 = ones(size(q11))*0.5;   y11(q11==1) = 1; y11(q11==3)=0; 
y12 = ones(size(q11))*0.5;   y12(q12==1) = 1; y12(q12==3)=0; 

y21 = zeros(size(q11));   y21(q21==1|y11==1) = 1;
y22 = zeros(size(q11));   y22(q22==1|y12==1) = 1; 


%% MAKE PLOTS FOR Q1
load BestZ % z c l p y mn sig
q=1; 
fcnMakeExplanatoryPlots(y11,y12,c,l,p,y,sig,q);

%% MAKE PLOTS FOR Q2
load BestZ2 % z c l p y mn sig
q=2; 
fcnMakeExplanatoryPlots(y21,y22,c,l,p,y,sig,q);
