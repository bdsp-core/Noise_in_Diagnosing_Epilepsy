function [y11,y12] = fcnGetData_EEG(T1,T2,ind);

q11 = T1(:,4:3:end); % Q1, t1
q12 = T2(:,2:3:end); % Q1, t2

q11 = q11(:,ind); 
q12 = q12(:,ind); 

% put into the form x(i,j,t) - person, question, time, for each question
y11 = table2array(q11)==2; 
y12 = table2array(q12)==2; 
