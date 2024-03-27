%% make gaussian fit and stacked bar plots
clear all; clc; format compact; 

%------------------------------------
%% QUESTION 1
%------------------------------------
load BestZ % gets:  z c l p y mn sig -- from Q1

% gaussian fits
figure(1); clf

spNo = 1; x= randn(1,50*20)*sig; titleStr = 'Occasion noise (ON)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 4; x= p(:); titleStr = 'Pattern noise (PN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 7; x= l; titleStr = 'Level noise (LN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 10; x= c; titleStr = 'Concensus variation (CV)';
fcnGaussianPlot(spNo,x,titleStr)

% noise bars
hold on
subplot(7,3,[13 16 19])
fcnPlotStackedBars(c,l,p,sig)

%------------------------------------
%% QUESTION 1b - Ordering EEG
%------------------------------------

load BestZ3 % gets:  z c l p y mn sig -- from Q1

% gaussian fits

spNo = 2; x= randn(1,50*20)*sig; titleStr = 'Occasion noise (ON)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 5; x= p(:); titleStr = 'Pattern noise (PN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 8; x= l; titleStr = 'Level noise (LN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 11; x= c; titleStr = 'Concensus variation (CV)';
fcnGaussianPlot(spNo,x,titleStr)

% noise bars
hold on
subplot(7,3,[14 17 20])
fcnPlotStackedBars(c,l,p,sig)


%------------------------------------
%% QUESTION 2
%------------------------------------
load BestZ2 % gets:  z c l p y mn sig -- from Q1

% gaussian fits

spNo = 3; x= randn(1,50*20)*sig; titleStr = 'Occasion noise (ON)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 6; x= p(:); titleStr = 'Pattern noise (PN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 9; x= l; titleStr = 'Level noise (LN)';
fcnGaussianPlot(spNo,x,titleStr)

spNo = 12; x= c; titleStr = 'Concensus variation (CV)';
fcnGaussianPlot(spNo,x,titleStr)

% noise bars
hold on
subplot(7,3,[15 18 21])
fcnPlotStackedBars(c,l,p,sig)