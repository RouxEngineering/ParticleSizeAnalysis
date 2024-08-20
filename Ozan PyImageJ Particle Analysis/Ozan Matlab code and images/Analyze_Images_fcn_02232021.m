function [d_eq, Area, Vols, minoraxis, majoraxis, circularity,...
    bins, histbins, dave, d_PD, d_CD, Vol_PD, Vol_CD, dpVol_PD] = ...
    Analyze_Images_fcn_02232021(fname, ext,threshold,pixsize,histbinsize)
%ProcessImage_fcn 
% This function processes is an image taken with a backlight to 
%   FUNCTION INPUTS
    % File Base Name: fname
    % File Extension: ext
    % Threshold to use in im2bw function to produce a binary image: threshold
    % Image Size in Millimeters (1x2 matrix): imagesize (currently unused)
    % Pixel Size (1x2) in micrometers: pixsize 
    % Histogram Bin Size: histbinsize
    % EXAMPLE
        % imagename = 'Image1.tif';
        % threshold = 0.5;
        % pixsize = [0.908 0.908]; % Size of each pixel in micrometers
        % histbinsize = 10; % Bin size of histogram in micrometers


% FUNCTION OUTPUTS
    % Equivalent particle size: d_eq (um)
    % Cross sectional are of particles: Area (um^2)
    % histogram bins: bins
    % histogram bin names: histbins
    % frequency based particle size distribution: d_PD
    % frequency based cumulative particle size distribution: d_CD
    % volume based particle size distribution: Vol_PD
    % volume based cumulative distribution: Vol_CD
    % Particles Size * Volume: dpVol_PD (used for volume averaged particle
    % size)
    % FIGURE WITH PROCESS INFORMATION
clf('reset')
imagename = [fname, ext];

% Create a Working Window
% Get Screen Size
ssize = get(0,'ScreenSize');
ssize(4) = ssize(4)*0.88;
f1 = figure(30);

set(f1, 'Position', ssize)
movegui('northwest');

% Import Image
image1 = imread(imagename);
image_1 = image1(:,:,1);
% imshow(image1);
image1_bw = im2bw(image1,threshold);
image1_bw = (image1_bw-1)*(-1); % Get the negative of the binary image to 
% work with white particles.

% f1 = figure(1);
f1;
subplot(2,3,1);
hold on
title('Unprocessed Image')
imshow(image1)
axis image;
hold off

f1;
subplot(2,3,2);
hold on
title('Binary Image')
imshow(image1_bw)
axis image; % so that the image is not artificially stretched
hold off

% Label Indiviual Items On the Image
labeledImage = bwlabel(image1_bw, 8); % Label each blob to make measurements

% Find Particles That Are At the Borders and Delete Them from Labeled Image

% Locate Blob Lables That Are at the Image Borders
top(:,1) = unique(labeledImage(1,:));
bottom(:,1) = unique(labeledImage(end,:));
left(:,1) = unique(labeledImage(:,1));
right(:,1) = unique(labeledImage(:,end));
A = [top; bottom; right; left];
B = nonzeros(A);
B = sort(B);
sremove = length(B(:,1));

rsize = length(image1_bw(:,1));
csize = length(image1_bw(1,:));
% New Black and White Image to be Processed Excluding Particles at Boundaries
image2_bw = image1_bw;


for k = 1:sremove
    for i = 1:rsize
        for j = 1:csize
            if B(k,1) == labeledImage(i,j)
                image2_bw(i,j) = 0;        
            end
        end
    end
end

% Create New Labeled Image
labeledImage2 = bwlabel(image2_bw, 8); % Label each blob to make measurements

% Assign colors to labeled images and plot
coloredLabels = label2rgb(labeledImage2, 'hsv', 'k', 'shuffle'); % pseudo random color labels

f1; % call figure to plot on
f1;
subplot(2,3,3);
hold on
title('Color Label of Idividual Particles (Particles on Edge are Removed)')
imshow(coloredLabels)
axis image; % so that the image is not artificially stretched
hold off

f1;
% Get all the blob properties.  Can only pass in originalImage in version R2008a and later.
particles = regionprops(labeledImage2, image2_bw, 'all');
N_particles = size(particles, 1);
% bwboundaries() returns a cell array, where each cell contains the row/column coordinates for an object in the image.
% Plot the borders of all the coins on the original grayscale image using the coordinates returned by bwboundaries.

hold off
% Get the boundaries of the blobs
boundaries = bwboundaries(image2_bw);
% 
    % Plot boundaries
% f2 = figure(2);
subplot(2,3,4);
imshow(image_1);
hold on
title('Measured Particles Are Circled on Original Image')
% set(f2, 'Position', ssize);
axis image;
for i = 1:N_particles
        plot(boundaries{i}(:,2),boundaries{i}(:,1),'r','LineWidth', 1);
end
hold off

% Record Measurements and Process Data
Area = zeros(N_particles,1);
d_eq = zeros(N_particles,1);
Vols = zeros(N_particles,1); 
minoraxis = zeros(N_particles, 1);
majoraxis = zeros(N_particles, 1);
circularity = zeros(N_particles,1);
A_scale = pixsize(1,1)*pixsize(1,2);
d_scale = pixsize(1,1);

for i = 1:N_particles
    Area(i,1) = particles(i).Area*A_scale; % micron^2
%     d_eq(i,1) = (particles(i).EquivDiameter)*d_scale; % micron
    d_eq(i,1) = sqrt(4*Area(i,1)/pi);
    Vols(i,1) = (4/3)*pi*((d_eq(i,1)/2)^3); % micron^3
    minoraxis(i,1) = particles(i).MinorAxisLength*d_scale; % micron
    majoraxis(i,1) = particles(i).MajorAxisLength*d_scale; % micron
    circularity(i,1) = (4*pi*Area(i,1))/((particles(i).Perimeter)^2);
end

% Create a Particle Size Histogram
bins(:,1) = 0:histbinsize:150; % Micrometers
Nbins = length(bins(:,1));
d_PD = zeros(Nbins-1,1); % Micrometers
dave = zeros(Nbins-1,1); % Mirometers
d_CD = zeros(Nbins-1,1); % Cumulative distribution
Vol_PD = zeros(Nbins-1,1); % micron^3
Vol_CD = zeros(Nbins-1,1); % micron^3
dpVol_PD = zeros(Nbins-1,1); % micron^4
Voltot = sum(Vols(:,1));

for i = 2:Nbins
    count = 0;
    dsum = 0;
    volume = 0;
    dpvolume = 0;
    for j = 1:N_particles
        if (d_eq(j,1) > bins(i-1,1)) && (d_eq(j,1)<= bins(i,1))
            count = count+1;
            dsum = dsum+d_eq(j,1);
            volume = volume + Vols(j,1);
            dpvolume = d_eq(j,1)*Vols(j,1) + dpvolume;
        end
    end
    d_PD(i-1,1) = count;
    dave(i-1,1) = dsum/count;
    Vol_PD(i-1,1) = volume;
    dpVol_PD(i-1,1) = dpvolume;
    if i == 2
        d_CD(i-1,1) = d_PD(i-1,1);
        Vol_CD(i-1,1) = Vol_PD(i-1,1);
    else
        d_CD(i-1,1) = d_CD(i-2,1)+d_PD(i-1,1);
        Vol_CD(i-1,1) = Vol_CD(i-2,1)+Vol_PD(i-1,1);
    end
end
% Normalize the volume distribution and volumetric cumulative distribution 
% Voldist = Voldist./Voltot;
Vol_CD = Vol_CD./Voltot;

% Normalize particle frequency based cumulative distribution
d_CD = d_CD./N_particles;

% Chart Names
histnames = cell(1,Nbins-1);
for i = 1:Nbins-1
        histnames{1,i} = [num2str(bins(i,1)),'-',num2str(bins(i+1,1)),' {\mu}m'];
end

histbins = categorical(histnames);
histbins = reordercats(histbins,histnames);

% Generate Particle Size Distribution Histogram
f1;
subplot(2,3,5);
bar(histbins, d_PD);

hold on 
title('Frequency Based Particle Size Histogram')
xlabel('Particle Size Range ({\mu}m)')
yyaxis left
ylabel('Particle Population')

yyaxis right
ylabel('Cumulative Distribution')
plot(d_CD)
% bar(Voldist);

hold off

% Generate Particle Size Distribution Histogram
f1;
subplot(2,3,6);
bar(histbins, Vol_PD);
hold on 
title('Volumetric Particle Size Distribution')
xlabel('Particle Size Range ({\mu}m)')
ylabel('Volumetric Fraction')

yyaxis right
plot(Vol_CD,'-r')
ylabel('Cumulative Distribution')
% plot(Volcumfit,'-b')
hold off


saveas(f1, ['ProcessedData_',fname], 'png');


end

