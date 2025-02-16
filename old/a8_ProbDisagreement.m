clear all; clc; format compact; 

% plot % agreement vs item difficulty, c
load Data; % T1, T2, T3, difficulty (1-4)

names = T1(:,1); 
y = T1(:,2); 
ind = find(difficulty>0); 
[y11,y12,y21,y22] = fcnGetData(T1,T2,ind);

figure(1); clf; 

%--------------------------
% fit for Q1
%--------------------------
sp = [1 3];
load BestZ % z c l p y mn

[c,pc,l,pl,pa] = fcnGetParmRelations(c,l,y11,y12);

subplot(2,2,sp(1)); 
plot(c',pc,'k+',c,pc,'k--','linewidth',2);
hold on;
plot(c',pc,'k+',c,pc,'k--','linewidth',2);
xlabel('Signal');
ylabel('% Yes')
set(gcf,'color','w')
grid on
axis([-4 4 0 1])
plot([-4,4],0.5*[1 1],'r--','LineWidth',2);
box off
title('Question 2')

subplot(2,2,sp(2)); 
plot(c',pa,'k+',c,pa,'k--','linewidth',2);
hold on;
% plot(c',pc,'k+',c,pc,'k--','linewidth',2);
xlabel('Signal');
ylabel('% Agreement')
set(gcf,'color','w')
grid on
axis([-4 4 0 1])
plot([-4,4],0.5*[1 1],'r--','LineWidth',2);
plot([-4,4],0.5*[1 1],'r--','LineWidth',2);
box off

%--------------------------
% fit for Q2
%--------------------------
load BestZ2 % z c l p y mn
sp = [2 4];

[c,pc,l,pl,pa] = fcnGetParmRelations(c,l,y21,y22);
p = polyfit(l, pl, 2);
xx = linspace(-4,4,100);
yy = polyval(p, xx);

subplot(2,2,sp(1)); 
plot(c',pc,'k+',c,pc,'k--','linewidth',2);
hold on;
plot(c',pc,'k+',c,pc,'k--','linewidth',2);
xlabel('Signal');
ylabel('% Yes')
set(gcf,'color','w')
grid on
axis([-4 4 0 1])
plot([-4,4],0.5*[1 1],'r--','LineWidth',2);
box off
title('Question 2')

subplot(2,2,sp(2)); 
plot(c',pa,'k+',c,pa,'k--','linewidth',2);
hold on;
% plot(c',pc,'k+',c,pc,'k--','linewidth',2);
xlabel('Signal');
ylabel('% Agreement')
set(gcf,'color','w')
grid on
axis([-4 4 0 1])
plot([-4,4],0.5*[1 1],'r--','LineWidth',2);
box off
