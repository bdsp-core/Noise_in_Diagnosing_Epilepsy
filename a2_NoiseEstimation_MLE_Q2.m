clear all; clc; format compact
warning off

%% get data
load Data; % T1, T2, T3, difficulty (1-4)
names = T1(:,1); 
% y = T1(:,2); 
ind = find(difficulty>0); 
[y11,y12,y21,y22] = fcnGetData(T1,T2,ind);

% try to get the marinals correct for i,j

%% yh
yh = mean([y21(:); y22(:)]);

%% l_i
x = [y21 y22]; 
li = mean(x,2);

%% c_j
x = [y21; y22];
cj = mean(x); 
ind = find(cj==0); cj(ind) = 0.01; 
ind = find(cj==1); cj(ind) = 0.99; 

%% p_ij
pij1 = y21+yh-(cj+li);
pij2 = y22+yh-(cj+li);
pij = (pij1+pij2)/2;

%% occasion noise: % different
pOcc = sum(y21(:)~=y22(:))/length(y21(:));

%%
c = log(cj./(1-cj)); 
% l = zeros(1,20);  
% p = zeros(20,50); 
% y = 0;
load BestZ2 % gets z c l p y mn

z = c+l+p+y; 

P1 = p+y-(c+l);

%%
mn = inf; 
c = log(cj./(1-cj)); c=c-mean(c); 
l=l-mean(l); 
p=p-mean(p(:)); 
o1 = randn(20,50)*0.1; 
o2 = randn(20,50)*0.1; 
% p=randn(20,50)*0.1; 
dn = 0; 
i=0; 
load BestZ2 % gets z c l p y mn

mn = 185;
while ~dn
    dy = randn*0.01;       
    dc = randn(20, 1) * 0.01;
    dl = randn(20, 1) * 0.01;
    dp = randn(20,50)*0.1;

    i=i+1; 
    yy=y+dy; 
    ll=l+dl; ll=ll-mean(ll); 
    pp=p+dp; pp=pp-mean(pp(:)); 
    cc=c+dc; cc=cc-mean(cc(:)); 
        
    z1=cc+ll+pp+yy; 
    
    p1 = 1./(1+exp(-z1));
    c1 = mean(p1,1);
    l1 = mean(p1,2);
    y1 = mean(p1(:));

    ec = abs(c1-cj); 
    el = abs(l1-li);
    eh = abs(yh-y1);
    LL = fcnGetLL_p(p1,y21,y22); 

    et = LL + max(ec) + max(el) + eh;
    if et<mn
        mn = et; 
        z = z1;   
        l=ll; l=l-mean(l); 
        y=yy; 
        p=pp;p=p-mean(p(:)); 
        
        figure(4); clf; 
        subplot(211); 
        bar([ec el' eh]);
        subplot(212); imagesc(p); 
        box off
        
        colormap gray
        drawnow
        disp(round([i LL]))
    end
    if ~mod(i,10000); 
        save BestZ2 z c l p y mn
    end
end
save BestZ2 z c l p y mn

%% find size of noise for o_ijt
load BestZ2 % z c l p y mn
p1 = []; p2 = [];
sig = linspace(1,5,100);
for i = 1:length(sig)
    [p1(i), p2(i)] = fcnGetOccNoise(sig(i),y21,y22,c,l,p,y); 
    disp([p1(i) p2(i)])
end
[ii,jj] = min(abs(p1-p2));
sig = sig(jj); 
save BestZ2 z c l p y mn sig
