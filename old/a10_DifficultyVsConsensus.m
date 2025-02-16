clear all; clc; format compact
warning off

%% get data
load Data; % T1, T2, difficulty (1-4)

for i = 1:size(T1,1); 
    T1.Participant{i} = 'xxx';
    T2.Participant{i} = 'xxx';
end
save Data T1 T2 difficulty

names = T1(:,1); 
% y = T1(:,2); 
ind = find(difficulty>0); 
[y11,y12,y21,y22] = fcnGetData(T1,T2,ind);
[qd1,qd2] = fcnGetSubjectiveDifficulty(T1,T2,ind);

x = [y11; y12];
cj = mean(x); 

[ii,jj] = sort(cj); 

figure(1); clf; 
subplot(311); imagesc(qd1(:,jj)); 
subplot(312); imagesc(qd2(:,jj));
colormap gray

x = [qd1; qd2];
dj = trimmean(x,50);

corrcoef(dj,cj)

figure(2); clf; 
% subplot(313); 
scatter(dj, cj, 100, 'fill');
xlabel('Perceived difficulty (average)')
ylabel('Consensus')
set(gcf,'Color','w')
grid on