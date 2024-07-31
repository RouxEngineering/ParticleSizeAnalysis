function [mic] = fcn_mic(fname,dpedges,psiedges)
%Processes Data From Microscope
mic.data = dlmread(fname,',',1,0);
mic.dp = mic.data(:,1);
mic.psi = mic.data(:,2);
mic.AR = mic.data(:,3);
mic.volp = (4*pi/3).*((mic.dp./2).^3);

mic.dpmean = mean(mic.dp(:,1));
mic.dpstd = std(mic.dp(:,1));
[mic.dpPD(:,1),mic.dpPDindex(:,1)] = histc(mic.dp(:,1),dpedges);
mic.dpPD = 100.*mic.dpPD/sum(mic.dpPD(:,1));
mic.dpCD = cumsum(mic.dpPD);
mic.volPD = zeros(length(dpedges(:,1)),1);
mic.volCD = zeros(length(dpedges(:,1)),1);

for i = 1:length(dpedges(:,1))
    for j = 1:length(mic.dp(:,1))
        if i == mic.dpPDindex(j,1)
            mic.volPD(i,1) = mic.volPD(i,1)+mic.volp(j,1);
        end
    end
    if i == 1
        mic.volCD(i,1) = mic.volPD(i,1);
    else
        mic.volCD(i,1) = mic.volCD(i-1,1)+mic.volPD(i,1);
    end
end

% Normalize volPD and volCD
mic.voltotal = sum(mic.volp(:,1));
mic.volPD = 100.*(mic.volPD./mic.voltotal);
mic.volCD = 100.*(mic.volCD./mic.voltotal);

mic.psimean = mean(mic.psi(:,1));
mic.psistd = std(mic.psi(:,1));

mic.dpmeans = zeros(length(dpedges(:,1))-1,1);
mic.dpstds = zeros(length(dpedges(:,1))-1,1);
mic.psimeans = zeros(length(dpedges(:,1))-1,1);
mic.psistds = zeros(length(dpedges(:,1))-1,1);

[mic.psiPD(:,1),mic.psiPDindex(:,1)] = histc(mic.psi(:,1),psiedges);
mic.psiPD = 100.*mic.psiPD/sum(mic.psiPD(:,1));
mic.psiCD = cumsum(mic.psiPD);

mic.classified.dp = cell(length(dpedges(:,1))-1,1);
mic.classified.psi = cell(length(dpedges(:,1))-1,1);
mic.classified.fitvals = zeros(length(dpedges(:,1))-1,2);
mic.classified.edges = psiedges(2:end,1); % remove far left boundary for CD plots
mic.classified.PD = cell(length(dpedges(:,1))-1,1);
mic.classified.CD = cell(length(dpedges(:,1))-1,1);
mic.classified.psiends = psiedges(2:end,1);
mic.distribute.psi(:,1) = 0.001:0.001:1;
mic.distribute.CD = zeros(length(mic.distribute.psi(:,1)),length(dpedges(:,1))-1);


mic.discrete.CD = [0.02,0.16,0.5,0.84,0.98];
mic.discrete.psi = zeros(length(dpedges(:,1))-1,5);
xmax = 1;

for i = 1:length(dpedges(:,1))-1
    dpclassified = mic.dp(mic.dp(:,1)>dpedges(i,1),1);
    psiclassified = mic.psi(mic.dp(:,1)>dpedges(i,1));
    mic.classified.dp{i}(:,1) = dpclassified(dpclassified<=dpedges(i+1,1),1);
    mic.classified.psi{i}(:,1) = psiclassified(dpclassified<=dpedges(i+1,1));
    mic.dpmeans(i,1) = mean(mic.classified.dp{i});
%     disp(['i = ',num2str(i),'-> ', num2str(mic.dpmeans(i,1))]);
    mic.dpstds(i,1) = std(mic.classified.dp{i});
    
    mic.psimeans(i,1) = mean(mic.classified.psi{i});
    mic.psistds(i,1) = std(mic.classified.psi{i});
    
%     PDsum = sum(mic.classified.psi{i});
    mic.classified.PD{i}(:,1) = histcounts(mic.classified.psi{i},psiedges);
    mic.classified.PD{i}(:,1) = mic.classified.PD{i}./sum(mic.classified.PD{i});
    mic.classified.CD{i}(:,1) = cumsum(mic.classified.PD{i});
    
    
    % Must set a maximum x value within the function to search for mu and
    % sig
    mic.classified.fitvals(i,:) = fminsearch(@(a) ...
        fit_fcn(a,mic.classified.psiends(:,1),mic.classified.CD{i}), [0.8 0.2]);
    
    mu = mic.classified.fitvals(i,1);
    sig = mic.classified.fitvals(i,2);
    
    for j = 1:length(mic.distribute.psi(:,1))
        
        mic.distribute.CD(j,i) = ...
            (0.5 + 0.5*erf((log(mic.distribute.psi(j,1))-mu)/(sqrt(2)*sig)))/...
            (0.5 + 0.5*erf((log(xmax)-mu)/(sqrt(2)*sig)));
    end
    
    %The distribution function behaves much better than a curve fit for
    %representing local cumulative distribution of sphericity.
%     mic.distribute.CD(:,i) = pchip(mic.classified.psiends(:,1),mic.classified.CD{i},mic.distribute.psi(:,1));
    
    

    indeces = mic.distribute.CD(:,i)>0.01 & ...
                mic.distribute.CD(:,i)<0.99;
    
    distribute_psi = mic.distribute.psi(indeces,1);
    distribute_CD = mic.distribute.CD(indeces,i);
    [distribute_CD, indeces2] = unique(distribute_CD);
    distribute_psi = distribute_psi(indeces2);
    
    
    if isempty(distribute_psi(:,1))
        mic.discrete.psi(i,:) = 1;
    else
        mic.discrete.psi(i,:) = pchip(distribute_CD,...
                distribute_psi,mic.discrete.CD(1,:));
    end
end

end

