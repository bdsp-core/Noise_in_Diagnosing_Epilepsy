function fcnPlotGoF(sp,Pr,li,l1,cj,c1,pij,P1)

subplot(3,2,sp(1))
L = mean(Pr,2); 
scatter(li,l1, 'filled', 'MarkerFaceAlpha', 1, 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'SizeData', 50);
hold on; 
xx = [0 1]; yy = [0 1]; plot(xx,yy,'--','linewidth',2);
axis square; box off; grid on
set(gca,'xticklabel','')
set(gca,'yticklabel','')
set(gca,'XTick',-1:.2:1)
set(gca,'YTick',-1:.2:1)
title('Consensus variation (CV)')

subplot(3,2,sp(2))
C = mean(Pr,1);
scatter(cj,c1, 'filled', 'MarkerFaceAlpha', 1, 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'SizeData', 50);
hold on; 
xx = [0 1]; yy = [0 1]; plot(xx,yy,'--','linewidth',2);
axis square; box off; grid on
set(gca,'xticklabel','')
set(gca,'yticklabel','')
set(gca,'XTick',-1:.2:1)
set(gca,'YTick',-1:.2:1)
title('Level noise (LN)')

subplot(3,2,sp(3))
scatter(pij(:),P1(:), 'filled', 'MarkerFaceAlpha', 1, 'MarkerEdgeColor', 'k', 'MarkerFaceColor', 'k', 'SizeData', 50);
hold on; 
xx = [0 1]; yy = [0 1]; plot(xx,yy,'--','linewidth',2);
xlabel('Observations'); ylabel('Model'); axis square; box off; grid on
set(gca,'XTick',-1:.5:1)
set(gca,'YTick',-1:.5:1)
set(gcf,'color','w');
title('Pattern noise (PN)')
