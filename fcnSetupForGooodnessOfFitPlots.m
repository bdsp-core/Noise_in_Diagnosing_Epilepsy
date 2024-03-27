function [Pr,li,l1,cj,c1,pij,P1] = fcnSetupForGooodnessOfFitPlots(y11,y12,c,l,p,y,sig)


%% yh
yh = mean([y11(:); y12(:)]);

%% l_i
x = [y11 y12]; 
li = mean(x,2);

%% c_j
x = [y11; y12];
cj = mean(x); 
ind = find(cj==0); cj(ind) = 0.01; 
ind = find(cj==1); cj(ind) = 0.99; 

%% p_ij
pij1 = y11+yh-(cj+li);
pij2 = y12+yh-(cj+li);
pij = (pij1+pij2)/2;

Y0 = (y11+y12)/2; 
L0 = li*ones(1,50);
C0 = ones(20,1)*cj; 
P0 = pij;
D0 = abs(y11-y12); 

% ****************
L = l*ones(1,50);
C = ones(20,1)*c; 
P = p;

dn=0; 
while ~dn
    Z = c+l+p+y;
    O1 = randn(20,50)*sig;
    O2 = randn(20,50)*sig; 
    Z1 = Z+O1;
    Z2 = Z+O2;
    P1 = 1./(1+exp(-Z1));
    P2 = 1./(1+exp(-Z2));
    y11 = P1>0.5; y12 = P2>0.5; 
    p1 = sum(y11(:)~=y12(:))/length(y11(:));
    p2 = sum(y11(:)~=y12(:))/length(y11(:));
    if abs(p1-p2)<0.01; dn=1; end
end

Z1 = C+L+P+O1; 
Z2 = C+L+P+O2;
P1 = 1./(1+exp(-Z1)); P2 = 1./(1+exp(-Z2)); 
Y1 = P1>0.5; Y2 = P2>0.5; 
D = abs(Y1-Y2);

Z = C+L+P+O1; 
Pr = 1./(1+exp(-Z));

% l_i
L = mean(Pr,2)*ones(1,50); 

% c_j
C = ones(20,1)*mean(Pr,1);

% yh
Yh = mean(Pr(:));

% p_ij
P = Pr+Yh-C-L;

[~,jj] = sort(c);
[~,ii] = sort(l); 

z1 = c+l+p+y;    
p1 = 1./(1+exp(-z1));
c1 = mean(p1,1);
l1 = mean(p1,2);
y1 = mean(p1(:));
P1 = p1+y1-(c1+l1);