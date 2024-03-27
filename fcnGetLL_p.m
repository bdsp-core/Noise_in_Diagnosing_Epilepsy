function LL = fcnGetLL_p(p1,y1,y2); 

% compute LL
p = p1(:);  

y=y1(:); LL1 = -sum( y.*log(p) + (1-y).*log(1-p));
y=y2(:); LL2 = -sum( y.*log(p) + (1-y).*log(1-p));
LL = (LL1+LL2)/2;