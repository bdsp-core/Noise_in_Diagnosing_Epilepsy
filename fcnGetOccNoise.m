function [p1, p2] = fcnGetOccNoise(sig,y11,y12,c,l,p,y); 

for i = 1:1000
    Z = c+l+p+y;
    Z1 = Z+randn(20,50)*sig; 
    Z2 = Z+randn(20,50)*sig; 
    P1 = 1./(1+exp(-Z1));
    P2 = 1./(1+exp(-Z2));
    Y11 = P1>0.5; Y12 = P2>0.5; 
    p1(i) = sum(y11(:)~=y12(:))/length(y11(:));
    p2(i) = sum(Y11(:)~=Y12(:))/length(Y11(:));
end
p1 = mean(p1); p2 = mean(p2); 
% subplot(421); imagesc(y11); subplot(422); imagesc(y12);
% subplot(423); imagesc(P1);  subplot(424); imagesc(P2);
% subplot(425); imagesc(Y11); subplot(426); imagesc(Y12); 
% subplot(427); imagesc(y11~=y12); 
% subplot(428); imagesc(Y11~=Y12);
