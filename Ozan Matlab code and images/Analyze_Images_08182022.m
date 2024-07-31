%% Process All Images in this Folder Using ProcessImage_fcn function
% Ozan Ozdemir, 09/29/2019

clear all 
close all
clc
% Label your images so that they are 'Image1.ext','Image2.ext',...

Nimages = 50; % number of images to process
basename = 'Image'; % base file name, Example: Image#, then label your images Image1, Image2, Image3, etc.
ext = '.png'; % enter file extension. .jpg, .tif, .png are common file extensions.
threshold = 0.5; % contrasting threshold. a number between 0 to 1.
pixsize = [0.172 0.172]; % micrometers per pixel
binsize = 5; % Particle size intervals for classifying powders given in ...
% micrometers. For CFD analysis, use small values. For presentations, use larger values.
outputFname = 'CP-Ti-APC.csv'; % Size Distribution Data File Name
outputFname2 = 'CP-Ti-APC-compiled-output.csv'; % File output size, and shape parameters for every individual particle



%% Process Images and Output Data
d = cell(Nimages,1);
Area = cell(Nimages,1);
Vols = cell(Nimages,1);
minoraxis = cell(Nimages,1);
majoraxis = cell(Nimages,1);
circularity = cell(Nimages,1);
bins = cell(Nimages,1);
histbins = cell(Nimages,1);
d_ave = cell(Nimages,1);
d_PD = cell(Nimages,1);
d_CD = cell(Nimages,1);
Vol_PD = cell(Nimages,1);
Vol_CD = cell(Nimages,1);
dpVol_PD = cell(Nimages,1);

samplesize = zeros(Nimages+1,1);
samplesize(1,1) = 0;

for i = 1:Nimages
    fname = [basename, num2str(i)];
    [d{i,1}, Area{i,1}, Vols{i,1}, minoraxis{i,1}, majoraxis{i,1}, ...
        circularity{i,1}, bins{i,1}, histbins{i,1},d_ave{i,1},...
        d_PD{i,1}, d_CD{i,1}, Vol_PD{i,1}, Vol_CD{i,1}, dpVol_PD{i,1}] = ...
        Analyze_Images_fcn_02232021(fname, ext,threshold,pixsize,binsize);
    samplesize(i+1,1) = samplesize(i,1)+length(d{i,1}(:,1));
end
close all

Nsamples = samplesize(end,1);
Nbins = length(bins{1,1}(:,1))-1;

% Compile All and Process Data
dcomp = zeros(Nsamples, 1); % compile particle diameter
Volcomp = zeros(Nsamples, 1); % compile particle volume
Acomp = zeros(Nsamples, 1); % compile particle shadow area
minoraxes = zeros(Nsamples, 1); %compile minor axes
majoraxes = zeros(Nsamples, 1); %compile major axes
circularities = zeros(Nsamples, 1); % compile circularities


for i = 1:Nimages
    dcomp(samplesize(i,1)+1:samplesize(i+1,1),1) = d{i,1};
    Volcomp(samplesize(i,1)+1:samplesize(i+1,1),1) = Vols{i,1};
    Acomp(samplesize(i,1)+1:samplesize(i+1,1),1) = Area{i,1};
    minoraxes(samplesize(i,1)+1:samplesize(i+1,1),1) = minoraxis{i,1};
    majoraxes(samplesize(i,1)+1:samplesize(i+1,1),1) = majoraxis{i,1};
    circularities(samplesize(i,1)+1:samplesize(i+1,1),1) = circularity{i,1};
end

psi1 = dcomp./majoraxes;
aspects = minoraxes./majoraxes;

Fs = (dcomp.^3)./((majoraxes.^(2.3)).*(minoraxes.^0.7));
Fn = (dcomp.^3)./((majoraxes.^2).*(minoraxes));

% ks = zeros(Nsamples,1);
% kn = zeros(Nsamples,1);
% 
% for i = 1:Nsamples
%     fun1 = @(var_ks)(var_ks-(Fs(i,1)^(1/3) + Fs(i,1)^(-1/3)));
%     fun2 = @(var_kn)(log(var_kn)-0.45*(-log(Fn(i,1)))^0.99);
%     x0 = 0.01;
%     x1 = 200;
%     ks(i,1) = fzero(fun1, [x0,x1]);
%     kn(i,1) = fzero(fun2, [x0,x1]);
% end 




% Categorize Data Into Defined Bins and Find Frequency and Volume Based
% Properties
d_PDs = zeros(Nbins-1,1); % Micrometers
daves = zeros(Nbins-1,1); % Mirometers
d_CDs = zeros(Nbins-1,1); % Cumulative distribution
Vol_PDs = zeros(Nbins-1,1); % micron^3
Vol_CDs = zeros(Nbins-1,1); % micron^3
dpVol_PDs = zeros(Nbins-1,1); % micron^4
dave_vols = zeros(Nbins-1,1); % micron
Voltot = sum(Volcomp(:,1)); 

minoraves = zeros(Nbins-1,1);
majoraves = zeros(Nbins-1,1);
aspectaves = zeros(Nbins-1,1);
ksaves = zeros(Nbins-1,1);
knaves = zeros(Nbins-1,1);


for i = 2:Nbins
    count = 0;
    dsum = 0;
    volume = 0;
    dpvolume = 0;
    
    minorsum = 0;
    majorsum = 0;
    aspectsum = 0;
%     knsum = 0;
%     kssum = 0;
    
    for j = 1:Nsamples
        if (dcomp(j,1) > bins{1,1}(i-1,1)) && (dcomp(j,1)<= bins{1,1}(i,1))
            count = count+1;
            dsum = dsum+dcomp(j,1);
            minorsum = minorsum + minoraxes(j,1);
            majorsum = majorsum + majoraxes(j,1);
%             kssum = kssum + ks(j,1);
%             knsum = knsum + kn(j,1);
            aspectsum = aspectsum + aspects(j,1);
            volume = volume + Volcomp(j,1);
            dpvolume = dcomp(j,1)*Volcomp(j,1) + dpvolume;
        end
    end
    d_PDs(i-1,1) = count;
    if count > 0
        minoraves(i-1,1) = minorsum/count;
        majoraves(i-1,1) = majorsum/count;
        aspectaves(i-1,1) = aspectsum/count;
%         ksaves(i-1,1) = kssum/count;
%         knaves(i-1,1) = knsum/count;
    end
    if count>0
        daves(i-1,1) = dsum/count;
        dave_vols(i-1,1) = dpvolume/volume;
    else
        daves(i-1,1) = mean(bins{1,1}(i,1),bins{1,1}(i-1,1));
        dave_vols(i-1,1) = mean(bins{1,1}(i,1),bins{1,1}(i-1,1));
    end
    Vol_PDs(i-1,1) = volume;
    dpVol_PDs(i-1,1) = dpvolume;
    
    if i == 2
        d_CDs(i-1,1) = d_PDs(i-1,1);
        Vol_CDs(i-1,1) = Vol_PDs(i-1,1);
    else
        d_CDs(i-1,1) = d_CDs(i-2,1)+d_PDs(i-1,1);
        Vol_CDs(i-1,1) = Vol_CDs(i-2,1)+Vol_PDs(i-1,1);
    end
end
% Normalize the volume distribution and volumetric cumulative distribution 
% Voldist = Voldist./Voltot;
Vol_CDs = Vol_CDs./Voltot;

% Normalize particle frequency based cumulative distribution
d_CDs = d_CDs./Nsamples;


% Overall Average Particle Size (Frequency Based)
dp_ave = sum(dcomp(:,1))/Nsamples;

% Overall Volume Based Particle Size 
dp_ave_vol = sum(dpVol_PDs(:,1))/Voltot;


%% Output Data
% Chart Names
histnames = cell(1,Nbins-1);
for i = 1:Nbins-1
        histnames{1,i} = [num2str(bins{1,1}(i,1)),'-',num2str(bins{1,1}(i+1,1)),' {\mu}m'];
end
histbins = categorical(histnames);
histbins = reordercats(histbins,histnames);

% Output Data File
CompiledData = [daves, d_PDs, d_CDs, dave_vols, Vol_PDs, Vol_CDs, dpVol_PDs];
headers = ['dp_ave (um), Probability Density, Cumulative Distribution',...
    ', Volume Based dp_ave (um), Volume Based Probability Density',...
    ', Volume Based Cumulative Distribution, dp*Vol_PD'];
%Open File and Write Headers to Files
fid = fopen(outputFname,'w');
fprintf(fid,'%s\r\n',headers);
fclose(fid);
%Append the data to the file
dlmwrite(outputFname, CompiledData,'-append','delimiter',',');
fclose('all');


% Plot Overall Results of the Particle Scans
f1 = figure(1);
ssize = get(0,'ScreenSize');
ssize(4) = ssize(4)*0.5;


set(f1, 'Position', ssize)
movegui('northwest');

subplot(1,2,1);
bar(histbins, d_PDs);
hold on
title('Overall Frequency Based Particle Size Distribution')
yyaxis left
xlabel('Particle Size Range ({\mu}m)')
ylabel('Particle Population')
yyaxis right
ylabel('Cumulative Distribution')
plot(d_CDs)
hold off

subplot(1,2,2);
bar(histbins, Vol_PDs);
hold on
title('Overall Volume Based Particle Size Distribution')
yyaxis left
xlabel('Particle Size Range ({\mu}m)')
ylabel('Volume in Bin ({\mu}m^{3})')
yyaxis right
ylabel('Cumulative Distribution')
plot(Vol_CDs)
hold off

saveas(f1, 'OverallResults','bmp')

% plot sphericity relationships
f2 = figure(2);
ssize = get(0,'ScreenSize');
ssize(4) = ssize(4)*0.5;
set(f2, 'Position', ssize)

subplot(1,2,1);
hold on
title('Particle Size vs. Sphericity');
xlabel('Particle Size (\mum)');
ylabel('Sphericity');
plot(dcomp(:,1), psi1(:,1), 'o');
hold off

subplot(1,2,2);
hold on
title('Sphericity Histogram');
xlabel('Sphericity');
ylabel('Population');
hist(psi1(:,1),15);
hold off


compiled_data = [dcomp, psi1, aspects];

fname_data = outputFname2;
fdata = fopen(fname_data,'w');
headers = ['Nominal Diameter (um), Sphericity, Aspect Ratio'];
fid = fopen(outputFname2,'w');
fprintf(fid,'%s\r\n',headers);
fclose(fid);
fclose('all');
dlmwrite(fname_data,compiled_data,'delimiter',',', '-append');


rowsofzero = aspectaves(:,1) == 0;
aspectaves(rowsofzero,:) = [];
daves(rowsofzero,:) = [];
minoraves(rowsofzero,:) = [];
majoraves(rowsofzero,:) = [];

figure(6)
cla reset
hold on 
title('Average Diameters vs Average Aspect Ratios')
xlabel('Average Diameters (\mum)');
ylabel('Average Aspect Ratios');
plot(dcomp(:,1), aspects(:,1),'o');
plot(daves(:,1), aspectaves(:,1),'-');
legend('Sphericity Data','Size Dependent Average');
hold off

%%
data = compiled_data;
Ndat = length(data(:,1)); % number of total data points (all equal)

cold = 1;
colpsi = 2;
colaspect = 3;


delbins = [5; 0.05; 0.05]; % binning size
Nvars = length(delbins(:,1)); % number of variables to be analyzed

binlims = [0, 80; 0, 1;0, 1];  % bin min and max
        
%Guess Mean and Deviation Params 
guess = [30 0.9; ... 
         0.8 0.2; ...
         0.8 0.2];
    
bins = cell(length(delbins(:,1)),1);    % generate a cell array for bins of variables
xaxis = cell(length(delbins(:,1)),1);    % generate a cell array for plotting binned data
Nbins = zeros(length(delbins(:,1)),1); % generate a numeric array for measuring number of bins in each array
binpops = cell(length(delbins(:,1)),1); % generate a cell array for storing populations in each bin
bincumpops = cell(length(delbins(:,1)),1); % generate a cell array for storing cumulative population in bins

% Generate bins, x axis, measure number of bins, generate cell array for
for i = 1:Nvars
    bins{i,1}(:,1) = binlims(i,1):delbins(i,1):(binlims(i,2)+delbins(i,1));
    xaxis{i,1} = bins{i,1}(2:end,1);
    Nbins(i,1) = length(xaxis{i,1}(:,1));
%     dcatnames = cell(length(delbins(:,1)),1);
end

for i = 1:Nvars % variable number
    for j = 1:Nbins(i,1)  % bin number
        count = 0; 
        for k = 1:Ndat % data number
            if (data(k,i) > bins{i,1}(j,1) && data(k,i) <= bins{i,1}(j+1,1))
                count = count+1;            
            end
        end
        binpops{i,1}(j,1) = count;
        if j == 1
            bincumpops{i,1}(j,1) = count;
        else
            bincumpops{i,1}(j,1) = count+bincumpops{i,1}(j-1,1);
        end
    end
    binpops{i,1} = binpops{i,1}./Ndat;
    bincumpops{i,1} = bincumpops{i,1}./Ndat;
end

% Log Normal Cumulative Distribution Curve Fit All Data
% Curve Fit
CDfitparams = zeros(Nvars,2);
LB = [0.05, 0.0002];
UP = [inf, inf];
for i = 1:Nvars
    CDfitparams(i,:) = fminsearch(@(a) fit_fcn(a,xaxis{i,1},bincumpops{i,1}), guess(i,:));  
end

% Generate Log Normal Curves
CD_fit = cell(Nvars,1);

for i = 1:Nvars
    CD_fit{i,1} = zeros(Nbins(i,1),1);
    for j = 1:Nbins(i,1)
        CD_fit{i,1}(j,1) = 0.5 + 0.5*erf(1+...
            (log(xaxis{i,1}(j,1))-log(CDfitparams(i,1)))/(sqrt(2)*CDfitparams(i,2))); 
    end
end



%% Call Function to Compute and Ouptput Sphericity Information
fcn_sphericity(outputFname2);


%% Plots
% Plot Processed Data and Curve Fits
ssize = get(0,'ScreenSize');
ssize(4) = ssize(4)*0.8;
f7 = figure(7);
set(f1, 'Position', ssize)
movegui('west');

xaxisnames = cell(Nvars,1);
yaxisnames = cell(Nvars,1);
xaxisnames{1,1} = 'Particle Size \mum';
xaxisnames{2,1} = 'Sphericities';
xaxisnames{3,1} = 'Aspect Ratio';
yaxisnameL = 'Probability Density';
yaxisnameR = 'Cumulative Density';

for i = 1:Nvars
    f7;
    subplot(2,3,i)
    hold on
    title(xaxisnames{i,1});
    xlabel(xaxisnames{i,1});
    ylabel(yaxisnameL);
    plot(xaxis{i,1}(:,1), binpops{i,1}(:,1),'+');
    
    yyaxis right
    ylabel(yaxisnameR);
    plot(xaxis{i,1}(:,1), bincumpops{i,1}(:,1),'ro');
    plot(xaxis{i,1}(:,1), CD_fit{i,1}(:,1),'k--');
    
    legend(yaxisnameL, yaxisnameR, 'Log-Normal Curve Fit');
end

%% Functions
% Function to Use for Fitting Data to Log Normal Distribution
function [SS] = fit_fcn(varin, xaxis, yaxis)
    binsize = length(xaxis(:,1));
    mu1 = varin(1);
    sig1 = varin(2);
%     disp(['Mean: ', num2str(mu1),' Sig: ', num2str(sig1)]);
 
    CD_fit = zeros(binsize,1);
    for i = 1:binsize
        CD_fit(i,1) = 0.5 + 0.5*erf(1+(log(xaxis(i,1))-log(mu1))/(sqrt(2)*sig1));    
    end
    diffs(:,1) = yaxis-CD_fit;
    squares(:,1) = diffs.^2;
    SS = sum(squares(:,1));
    disp(['Sum of Squares: ',num2str(SS)]);
end




