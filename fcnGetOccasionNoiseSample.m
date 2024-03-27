function [O1,O2] = fcnGetOccasionNoiseSample(c,l,p,y,y11,y12,sig)

for i = 1:1000
    Z = c+l+p+y;
    O1 = randn(20,50)*sig; 
    O2 = randn(20,50)*sig; 
    Z1 = Z+O1;
    Z2 = Z+O2;
    P1 = 1./(1+exp(-Z1));
    P2 = 1./(1+exp(-Z2));
    Y11 = P1>0.5; Y12 = P2>0.5; 
    p1(i) = sum(y11(:)~=y12(:))/length(y11(:));
    p2(i) = sum(Y11(:)~=Y12(:))/length(Y11(:));
end
p1 = mean(p1); p2 = mean(p2); 

ON1 = O1; 
ON2 = O2; 