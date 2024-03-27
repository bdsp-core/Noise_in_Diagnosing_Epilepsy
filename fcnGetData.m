function [y11,y12,y21,y22] = fcnGetData(T1,T2,ind);

q11 = T1(:,4:3:end); % Q1, t1
q21 = T1(:,5:3:end); % Q2, t1

q12 = T2(:,2:3:end); % Q1, t2
q22 = T2(:,3:3:end); % Q2, t2

q11 = q11(:,ind); q21 = q21(:,ind); 
q12 = q12(:,ind); q22 = q22(:,ind); 

% put into the form x(i,j,t) - person, question, time, for each question
y11 = table2array(q11)==1; 
y12 = table2array(q12)==1; 

y21 = table2array(q21)==1 | y11==1; 
y22 = table2array(q22)==1 | y12==1; 