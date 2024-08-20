
clear all
close all
clc

% Call mic_fcn 
fname = 'CP-Ti-APC-compiled-output.csv';

% Histogram Limits
dpmin = 0;
dpmax = 70;
dpint = 5;

% Histogram Limit Calculations
dpedges(:,1) = dpmin:dpint:dpmax;
psiedges(:,1) = 0:0.1:1;

[mic] = fcn_mic(fname,dpedges,psiedges);
[colors,lines,markers] = fcn_colors();

% Generate Plots and Print Files
%Figure 1
f1 = figure(1); 
ssize = get(0,'screensize');
ssize(3) = ssize(3)*0.75;
ssize(4) = ssize(4)*0.25;
f1.Position = ssize;

font = 'Arial';
fontsize = 16;
linewidth = 1.5;

subplot(1,3,1)
hold on 
xlabel('Particle Size, (\mum)')
ylabel('Particle Sphericity, \Psi')
p0 = plot(mic.dp,mic.psi,'.');
for i = 1:5
    p(i) = plot(mic.dpmeans,mic.discrete.psi(:,i));
    p(i).Marker = markers{i};
    p(i).LineStyle = lines{i};
    p(i).LineWidth = linewidth;
    p(i).Color = 'k';
end
p(3).LineStyle = '-';
p(3).Color = 'r';
lgd = legend('Data','2nd %tile','16th %tile','50th %tile',...
    '84th %tile','98th %tile');
lgd.FontSize = fontsize;
lgd.Location = 'SouthEast';
lgd.Visible = 'off';
xlim([0,80])
ylim([0,1])
ax = gca;
ax.FontSize = fontsize;
ax.Box = 'on';
ax.LineWidth = linewidth;
hold off
pause(0.1)
std1low = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,2));
std1high = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,4));
std2low = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,1));
std2high = abs(mic.discrete.psi(:,3)-mic.discrete.psi(:,5));

subplot(1,3,2)
hold on 
xlabel('Particle Size, (\mum)')
ylabel('Particle Sphericity, \Psi')
p0 = plot(mic.dp,mic.psi,'.');
for i = 1:5
    p(i) = plot(mic.dpmeans,mic.discrete.psi(:,i));
    p(i).Marker = markers{i};
    p(i).LineStyle = lines{i};
    p(i).LineWidth = linewidth;
    p(i).Color = 'k';
end
p(3).LineStyle = '-';
p(3).Color = 'r';
xlim([0,80])
ylim([0,1])
lgd = legend('Data','2nd %tile','16th %tile','50th %tile',...
    '84th %tile','98th %tile');
lgd.FontSize = fontsize;
lgd.Location = 'SouthEast';
ax = gca;
ax.FontSize = fontsize;
ax.Box = 'on';
ax.LineWidth = linewidth;
hold off
pause(0.1)

subplot(1,3,3)
hold on
xlabel('Particle Size (\mum)')
ylabel('Particle Sphericity, \Psi')
hold on
for i = 1:length(dpedges(:,1))-1
    plot(mic.classified.dp{i},mic.classified.psi{i},'.','color',colors.matte{i});
end
ax = gca;
ax.FontSize = fontsize;
hold off

% Figure 2
f2 = figure(2); 
ssize = get(0,'screensize');
ssize(3) = ssize(3)*1;
ssize(4) = ssize(4)*0.9;
f2.Position = ssize;

for i = 1:length(dpedges(:,1))-1
    subplot(3,5,i)
    hold on
    title(['d_p = (',num2str(dpedges(i,1)),',',num2str(dpedges(i+1,1)),'] \mum']);
    xlabel('Particle Sphericity, \Psi')
    ylabel('Cumulative Density (%)')
    plot(mic.classified.edges(:,1),100.*mic.classified.CD{i},'*');
    plot(mic.distribute.psi(:,1),100.*mic.distribute.CD(:,i),'color',colors.matte{1});
    plot(mic.discrete.psi(i,:),100.*mic.discrete.CD(1,:),'r.')
    ax = gca;
    ax.FontSize = fontsize;
    hold off
end

subplot(3,5,15)
hold on
title(['d_p = (',num2str(dpedges(i,1)),',',num2str(dpedges(i+1,1)),'] \mum']);
xlabel('Particle Sphericity, \Psi')
ylabel('Cumulative Density (%)')
plot(200,200,'*');
plot(200,200,'color',colors.matte{1});
plot(200,200,'r.')
xlim([0 1]);
ylim([0 100]);
legend('\Psi, CD Data','\Psi, CD Log-Normal Fit',...
    '\Psi_i = [CD_i = 2%,16%,50%,84%,98%]')
ax = gca;
ax.FontSize = fontsize;
hold off
    
fnameout = 'Size_Dependent_Sphericity_CDs.txt';
header = 'dp, PD(%), psimean, 2%, 16%, 50%, 84%, 98%,mu,sigma';
output = [mic.dpmeans(:,1),mic.volPD(1:end-1,1), mic.psimeans(:,1), ...
    mic.discrete.psi,mic.classified.fitvals(:,1),mic.classified.fitvals(:,2)];
dlmwrite(fnameout,header,'');
dlmwrite(fnameout,output,'delimiter',',','-append');

saveas(f1,'Figure1_v2.png');
saveas(f2,'Figure2_v2.png');
    
    
    
    
    
    
    