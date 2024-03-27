function [c,pc,l,pl,pa] = fcnGetParmRelations(c,l,y11,y12)

pc1 = mean(y11,1);
pc2 = mean(y12,1); 
pc = (pc1+pc2)/2; 
[~,jj] = sort(c);
c = c(jj); 
pc = pc(jj); 

pl1 = mean(y11,2);
pl2 = mean(y12,2); 
pl = (pl1+pl2)/2; 
[~,ii] = sort(l);
l = l(ii); 
pl = pl(ii); 

% percent agreement - cases
for i = 1:length(c); 
    x = y11(:,i); y = y12(:,i); 
    num = 0; den = 0; 
    for j = 1:length(x); 
        for k = 1:length(y); 
            den=den+1;
            num=num+(x(j)==y(k));
        end
    end
    pa(i) = num/den; 
end
pa = pa(jj);
