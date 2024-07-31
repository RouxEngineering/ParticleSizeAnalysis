
function [] = fcn_sphericity(fname)

% Call mic_fcn 
% fname = 'Valimet-Al6061-Compiled-Particle-Data.csv';

% Histogram Limits
dpmin = 0;
dpmax = 70;
dpint = 5;

% Histogram Limit Calculations
dpedges(:,1) = dpmin:dpint:dpmax;
psiedges(:,1) = 0:0.05:1;

[mic] = fcn_mic(fname,dpedges,psiedges);
[colors,~,~] = fcn_colors();

% Generate Plots and Print Files
%Figure 1
% f10 = figure(10); 
% ssize = get(0,'screensize');
% ssize(3) = ssize(3)*0.75;
% ssize(4) = ssize(4)*0.25;
% f10.Position = ssize;

% subplot(1,3,1)
% hold on
% xlabel('Particle Size, (\mum)')
% ylabel('Particle Sphericity, \Psi')
% plot(mic.dp,mic.psi,'.')
% errorbar(mic.dpmeans,mic.psimeans,mic.psistds)
% xlim([0.3,70])
% ylim([0,1])
% hold off
% pause(0.1)

std1low = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,2));
std1high = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,4));
std2low = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,1));
std2high = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,5));

f10 = figure(10);
linewidth = 1.25;
markersize = 5;
set(gca,'FontSize',13')
hold on 
xlabel('Particle Size, (\mum)')
ylabel('Particle Sphericity, \Psi')
p = plot(mic.dp,mic.psi,'.','color',colors.matte{1});
p.MarkerSize = markersize;
p.LineWidth = linewidth;
ebar = errorbar(mic.dpmeans,mic.discrete.psi(:,3),std2low,std2high,...
    'linestyle','none','color',colors.matte{3});
ebar.MarkerSize = markersize;
ebar.LineWidth = linewidth;
ebar = errorbar(mic.dpmeans, mic.discrete.psi(:,3),std1low,std1high,...
    '-','color',colors.matte{2});
ebar.Marker = '^';
ebar.MarkerSize = markersize;
ebar.LineWidth = linewidth;
xlim([0,70])
ylim([0,1])
legend('Data','±2\sigma','\psi_{mean} ±1\sigma','Location','SouthEast')
hold off
pause(0.1)
saveas(f10,'SizeVSphericity.png');
% 
% subplot(1,3,3)
% hold on
% xlabel('Particle Size (\mum)')
% ylabel('Particle Sphericity, \Psi')
% hold on
% for i = 1:length(dpedges(:,1))-1
%     plot(mic.classified.dp{i},mic.classified.psi{i},'.','color',colors.matte{i});
% end
% hold off

% Figure 2
f20 = figure(20); 
ssize = get(0,'screensize');
ssize(3) = ssize(3)*0.8;
ssize(4) = ssize(4)*0.9;
f20.Position = ssize;

for i = 1:length(dpedges(:,1))-1
    subplot(4,5,i)
    hold on
    title(['d_p = (',num2str(dpedges(i,1)),',',num2str(dpedges(i+1,1)),'] \mum']);
    xlabel('Particle Sphericity, \Psi')
    ylabel('Cumulative Density (%)')
    plot(mic.classified.edges(:,1),100.*mic.classified.CD{i},'*');
    plot(mic.distribute.psi(:,1),100.*mic.distribute.CD(:,i),'color',colors.matte{1});
    plot(mic.discrete.psi(i,:),100.*mic.discrete.CD(1,:),'r.')
    hold off
end

% subplot(4,5,20)
% hold on
% title(['d_p = (',num2str(dpedges(i,1)),',',num2str(dpedges(i+1,1)),'] \mum']);
% xlabel('Particle Sphericity, \Psi')
% ylabel('Cumulative Density (%)')
% plot(200,200,'*');
% plot(200,200,'color',colors.matte{1});
% plot(200,200,'r.')
% xlim([0 1]);
% ylim([0 100]);
% legend('\Psi, CD Data','\Psi, CD Log-Normal Fit',...
%     '\Psi_i = [CD_i = 2%,16%,50%,84%,98%]')
% hold off
%     
fnameout = 'Size_Dependent_Sphericity_CDs.txt';
header = 'dp, PD(%), psimean, Percentile: 2%, Percentile: 16%, Percentile: 50%, Percentile: 84%, Percentile: 98%,mu,sigma';
output = [mic.dpmeans(:,1),mic.volPD(1:end-1,1), mic.psimeans(:,1), ...
    mic.discrete.psi,mic.classified.fitvals(:,1),mic.classified.fitvals(:,2)];
dlmwrite(fnameout,header,'');
dlmwrite(fnameout,output,'delimiter',',','-append');

end
    
    
    
    
    
    
    
    
    
    