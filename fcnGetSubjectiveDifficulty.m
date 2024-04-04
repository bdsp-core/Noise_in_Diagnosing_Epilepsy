function [qd1,qd2] = fcnGetSubjectiveDifficulty(T1,T2,ind);

qd1 = T1(:,6:3:end); % perceived difficulty
qd2 = T2(:,4:3:end); % perceived difficulty

qd1 = table2array(qd1); 
qd2 = table2array(qd2); 
