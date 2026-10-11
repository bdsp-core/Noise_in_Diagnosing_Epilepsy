clear all; clc; format compact; 

% plot % agreement vs item difficulty, c
load Data; % T1, T2, T3, difficulty (1-4)

names = T1(:,1); 
y = T1(:,2); 
ind = find(difficulty>0); 
[y11,y12,y21,y22] = fcnGetData(T1,T2,ind);

q11 = table2array(T1(:,4:3:end)); % Q1, t1
q21 = table2array(T1(:,5:3:end)); % Q2, t1

q12 = table2array(T2(:,2:3:end)); % Q1, t2
q22 = table2array(T2(:,3:3:end)); % Q2, t2

% question 1
% percent 1,2,3 by question

%% percentage of yes answers, dunno, no - by case
% question 1
disp('% percentage of yes answers, dunno, no - by case: Q1')
p1 = sum(q11==1); p2 = sum(q12==1); p = [p1 p2]; disp([min(p) max(p) min(p)/20*100 max(p)/20*100]);
p1 = sum(q11==2); p2 = sum(q12==2); p = [p1 p2]; disp([min(p) max(p) min(p)/20*100 max(p)/20*100]);
p1 = sum(q11==3); p2 = sum(q12==3); p = [p1 p2]; disp([min(p) max(p) min(p)/20*100 max(p)/20*100]);
disp('--------------')
% question 2
disp('% percentage of yes answers, dunno, no - by case: Q2')
p1 = sum(y21==1); p2 = sum(y22==1); p = [p1 p2]; disp([min(p) max(p) min(p)/20*100 max(p)/20*100]);
p1 = sum(y21==0); p2 = sum(y22==0); p = [p1 p2]; disp([min(p) max(p) min(p)/20*100 max(p)/20*100]);

%% percentage of yes - by expert
% question 1
disp('percentage of yes - by expert: Q1'); 
p1 = sum(q11==1,2); p2 = sum(q12==1,2); p = [p1; p2]; disp([min(p) max(p) min(p)/50*100 max(p)/50*100]);
p1 = sum(q11==3,2); p2 = sum(q12==3,2); p = [p1; p2]; disp([min(p) max(p) min(p)/50*100 max(p)/50*100]);
disp('--------------')
% question 2
disp('percentage of yes - by expert: Q2'); 
p1 = sum(y21==1,2); p2 = sum(y22==1,2); p = [p1; p2]; disp([min(p) max(p) min(p)/50*100 max(p)/50*100]);
p1 = sum(y21==0,2); p2 = sum(y22==0,2); p = [p1; p2]; disp([min(p) max(p) min(p)/50*100 max(p)/50*100]);

%% number of times changing mind
disp('--------------')
disp('% number of times changing mind: Q1'); 
n = sum(q11(:)~=q12(:)); disp([n n/length(q11(:))*100]);
disp('% number of times changing mind: Q2'); 
n = sum(y11(:)~=y12(:)); disp([n n/length(q11(:))*100]);

%% how often did each expert change their mind?
disp('--------------')
disp('%% how often did each expert change their mind?: Q1')
n = sum(q11~=q12,2)'; disp(round([mean(n) min(n) max(n) mean(n)*2 min(n)*2 max(n)*2]));
disp('%% how often did each expert change their mind?: Q2')
n = sum(y11~=y12,2)'; disp(round([mean(n) min(n) max(n) mean(n)*2 min(n)*2 max(n)*2]));

%% which cases generate the most mind-changing?
disp('--------------')
disp('%% which cases generate the most mind-changing?: Q1')
n = sum(q11~=q12,1); disp(round([mean(n) min(n) max(n) mean(n)*5 min(n)*5 max(n)*5]));
disp('%% which cases generate the most mind-changing?: Q2')
n = sum(y11~=y12,1); disp(round([mean(n) min(n) max(n) mean(n)*5 min(n)*5 max(n)*5]));


%%  accuracy (agreement with consensus)
disp('--------------')
disp('%%  accuracy (agreement with consensus): Q1')
% correct answer: consensus
m = mean([y11; y12]); 
y=m>=0.5;
% % agreement with correct 
pa1 = mean([y11 y12]==[y y],2); 
disp([median(pa1) min(pa1) max(pa1)])

disp('%%  accuracy (agreement with consensus): Q2')
y=m>=0.5;
% % agreement with correct 
pa2 = mean([y21 y22]==[y y],2);
disp([median(pa2) min(pa2) max(pa2)])

%% correlation between consistency and accuracy
disp('--------------')
disp('%% correlation between consistency and accuracy')
con1 = sum(y11==y12,2)/50;
con2 = sum(y21==y22,2)/50;
[c1,p1] = corr(con1,pa1);
[c2,p2] = corr(con2,pa2);
disp([c1 p1 c2 p2])

%% correlation between years experience and accuracy
disp('--------------')
disp('%% correlation between years experience and accuracy')
ye = T1.HowManyYearsHaveYouBeenReadingEEGsincludingDuringClinicalNeurop;
[c1,p1] = corr(ye,pa1);
[c2,p2] = corr(ye,pa2);
disp([c1 p1 c2 p2])

%% ------------------------------------
% --------- CLINICAL DX --------------
% ------------------------------------
% get clinical diagnoses
load finalDx % finalDx

%% agreement between clinical dx and consensus dx
disp('--------------')
disp('%% agreement between clinical dx and consensus dx')
yClin = finalDx.VarName2';
m = mean([y21; y22]); 
y=m>=0.5;
n = sum(yClin==y);
pa = n/50; 
disp([n pa]);

% Q1
disp('--------------')
consensus2 = mean([y21; y22],1);
[c,p] = corr(consensus2',yClin');
disp('correlation: clinical dx, consensus dx')
disp([c p])

i0 = find(yClin==0);
t1 = y21(:,i0); t2 = y22(:,i0);
t1 = t1(:); t2=t2(:); t=[t1 ; t2];
p0=sum(t==0)/length(t);

i1 = find(yClin==1);
t1 = y21(:,i1); t2 = y22(:,i1);
t1 = t1(:); t2=t2(:); t=[t1 ; t2];
p1=sum(t==1)/length(t);
disp('% correct (vs clinical dx): 0, 1')
disp([p0 p1])


%%  accuracy (agreement with clinical dx)
disp('--------------')
% correct answer: consensus
% % agreement with correct 
y = yClin;

pa2 = mean([y21 y22]==[y y],2);
disp('accuracy (agreement with clinical dx)')
disp([median(pa2) min(pa2) max(pa2)])

%% correlation between consistency and accuracy - clin
disp('--------------')
con2 = sum(y21==y22,2)/50;
[c2,p2] = corr(con2,pa2);
disp('correlation between consistency and accuracy - clin')
disp([c2 p2])

%% correlation between years experience and accuracy - clin
disp('--------------')
ye = T1.HowManyYearsHaveYouBeenReadingEEGsincludingDuringClinicalNeurop;
[c2,p2] = corr(ye,pa2);
disp('correlation between years experience and accuracy - clin')
disp([c2 p2])

%%----------------------------------------
%%----------------------------------------
% WITHIN AND BETWEEN EXPERT VARIABILITY
%%----------------------------------------
% look at how many agree - final dx
disp('--------------')
m1 = sum([y21]);
m2 = sum([y22]);
disp([m1;m2]);

%% Between-expert variance vs within-expert inconsistency: these are case measures
disp('--------------')

% between-expert agreement
for i = 1:50
    num = 0; den = 0; ct=0; 
    for j = 1:20
        for k = (j+1):20
            num = num+ (y21(j,i)==y21(k,i)) + (y22(j,i)==y22(k,i));
            den = den+2; 
        end
    end
    bea(i) = num/den; 
end

% within-expert agreement
wea = mean(y21==y22);

disp('Correlation: within-expert agreement vs between expert agreement')
[r,p] = corr(wea',bea');
disp([r p])

%% correlate between-expert variance & within-expert inconsistence with rate of requesting EEG
disp('--------------')

rre = sum([q11==2; q12==2],1)/40;

disp('correlation: within-expert agreement vs rate of requesting EEG')
[r,p] = corr(wea',rre');
disp([r p])

disp('correlation: between-expert agreement vs rate of requesting EEG')
[r,p] = corr(rre',bea');
disp([r p])

%%-----------------------
% EEG ordering
%------------------------
disp('--------------')
% number of EEGs requested both times
nBoth = sum(sum(q11==2 & q12==2)); 
% number of EEGs requested just one time
nOne = sum(sum( (q11==2 & q12~=2) | (q11~=2 & q12==2)));
% number of EEGs requested just one time
nNone = sum(sum(q11~=2 & q12~=2));
disp('Number requesting EEG none, one, both times')
disp([nBoth nOne nNone])

%% check consistency in "none" cases
disp('--------------')
ind = (q11(:)~=2 & q12(:)~=2);
nSame = sum(q11(ind)==q12(ind));
pSame = nSame/sum(ind)*100;
disp('check consistency in "none" cases')
disp([nSame pSame])

% calculate between-expert agreement
num = 0; den = 0;
for i = 1:50 % cases
    for j = 1:20
        for k = (j+1):20
            if q11(j,i)~=2 & q12(k,i)~=2;
                den=den+1; 
                if q11(j,i)==q12(k,i)
                    num=num+1; 
                end
            end
        end
    end
end
disp('between-expert agreement - none cases ')
pa = num/den;
disp(pa)

%% check consistency in "one" cases
disp('--------------')
Q11 = q11(:); Q12 = q12(:); 
ind = find( (Q11==2 & Q12~=2) | (Q11~=2 & Q12==2));
Q21 = y21(:); Q22 = y22(:); 
nSame = sum(Q21(ind)==Q22(ind));
pSame = nSame/length(ind)*100;
disp('check consistency in "One" cases')
disp([nSame pSame])

% calculate between-expert agreement
num = 0; den = 0;
for i = 1:50 % cases
    for j = 1:20
        for k = (j+1):20
            if ((q21(j,i)~=2 & q12(k,i)==2) | (q21(j,i)~=2 & q22(k,i)==2));
                den=den+1; 
                if y21(j,i)==y12(k,i)
                    num=num+1; 
                end
            end
        end
    end
end
pa = num/den;
disp('between-expert agreement - One cases ')
disp(pa)

%% Effect of EEG + MRI: compare rate of diagnoses with vs without
disp('--------------')
Q11 = q11(:); Q12 = q12(:); 

ind1 = find( (Q11~=2 & Q12==2) ); % no EEG on occasion 1, + on occ 2
nWithout1 = sum(y11(ind1)==1); dWithout1 = length(ind1); 
nWith1 = sum(y22(ind1)==1); dWith1 = length(ind1); 

ind2 = find( (Q11==2 & Q12~=2) ); % no EEG on occasion 2, + on occ 1
nWithout2 = sum(y12(ind2)==1); dWithout2 = length(ind2); 
nWith2 = sum(y21(ind2)==1); dWith2 = length(ind2); 

nWithout = nWithout1 + nWithout2;
nWith = nWith1 + nWith2; 
pWithout = nWithout / (dWithout1+dWithout2); 
pWith = nWith / (dWith1+dWith2); 

disp('Probability dx with vs without EEG (One cases)')
disp([pWithout pWith])

disp('--------------')
% correlation of with vs without EEG with diagnostic accuracy
m = mean([y21; y22]); 
y=m>=0.5;

% get diagnoses without EEG
num = 0; den = 0; 
for i = 1:20; 
    for j = 1:50; % cases
        if q11(i,j)~=2; 
            num = num + (y11(i,j)==y(j));
            den = den + 1; 
        end
        if q12(i,j)~=2; 
            num = num + (y12(i,j)==y(j));
            den = den + 1; 
        end
    end
end
pCorrectWithout1 = num/den;

% get diagnoses without EEG
num = 0; den = 0; 
for i = 1:20; 
    for j = 1:50; % cases
        if q11(i,j)==2; 
            num = num + (y21(i,j)==y(j));
            den = den + 1; 
        end
        if q12(i,j)==2; 
            num = num + (y22(i,j)==y(j));
            den = den + 1; 
        end
    end
end
pCorrectWith1 = num/den;
disp('Probability correct with vs without EEG (One cases) - vs consensus')
disp([pCorrectWith1 pCorrectWithout1])

% other measure of accuracy -- final dx

y=yClin;

% get diagnoses without EEG
num = 0; den = 0; 
for i = 1:20; 
    for j = 1:50; % cases
        if q11(i,j)~=2; 
            num = num + (y11(i,j)==y(j));
            den = den + 1; 
        end
        if q12(i,j)~=2; 
            num = num + (y12(i,j)==y(j));
            den = den + 1; 
        end
    end
end
pCorrectWithout1 = num/den;

% get diagnoses without EEG
num = 0; den = 0; 
for i = 1:20; 
    for j = 1:50; % cases
        if q11(i,j)==2; 
            num = num + (y21(i,j)==y(j));
            den = den + 1; 
        end
        if q12(i,j)==2; 
            num = num + (y22(i,j)==y(j));
            den = den + 1; 
        end
    end
end
pCorrectWith1 = num/den;
disp('Probability correct with vs without EEG (One cases) -- vs clinical dx')
disp([pCorrectWith1 pCorrectWithout1])


%% check consistency in "both" cases
disp('--------------')
ind = (q11(:)==2 & q12(:)==2);
nSame = sum(q21(ind)==q22(ind));
pSame = nSame/sum(ind)*100;
disp('check consistency in "Both" cases')
disp([nSame pSame])

% calculate between-expert agreement
num = 0; den = 0;
for i = 1:50 % cases
    for j = 1:20
        for k = (j+1):20
            if q11(j,i)==2 & q12(k,i)==2;
                den=den+1; 
                if q21(j,i)==q22(k,i)
                    num=num+1; 
                end
            end
        end
    end
end
pa = num/den;
disp('between-expert agreement - Both cases ')
disp(pa)

%% study participants
ye = T1.HowManyYearsHaveYouBeenReadingEEGsincludingDuringClinicalNeurop;
disp('Years experience: min, max, median')
disp([min(ye) max(ye) median(ye)])

%% save for python

T1_struct = struct(T1);
T2_struct = struct(T2);
save('Data_struct.mat', 'T1_struct', 'T2_struct', 'difficulty');
