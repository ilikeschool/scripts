%
exp='small_1p2_slow';
%exp='small_2p4_slow';
%exp='small_1p2_fast';
%exp='small_2p4_fast';
fileName=[exp '.xls'];
fileName_pdf=['plots/' exp];
delete([fileName_pdf '.pdf'])
%
specs={'UGF','PM','DCG','IDD','PSR_20K','REGOUT','TIN','VCC','VREF','IREF','IREG','VREG','LPM','IPD'};
scales=[1e-6 1 1 1e6 1 1 1e6 1 1 1e6 1e3 1e3 1 1e9];
yaxLabels={'MHz','deg','dB','uA','dB','V','uV','V','V','uA','uV / mA','mV / V','deg','nA'};
legLocs=[2 2 2 1 1 1 1 2 1 1 4 2 1 1];
%
it=1;
%
for it=1:length(specs)
   specIndx=it;
   spec=specs{specIndx};
   scale=scales(specIndx);
   yaxLabel=yaxLabels(specIndx);
   legLoc=legLocs(specIndx);
   labels={'F' 'F' 'F' 'F' 'F' 'F' 'L' 'H';'S' 'S' 'S' 'S' 'S' 'S' 'H' 'C'};
   [corners,parameters,measures]=readMeasures(fileName,[1:8],[],[],spec);
   [deltas,indx_sort]=sortMeasures(measures,corners);
   parameters(indx_sort)
   deltas
   [measure,tickLabel,xaxLabel,legendText]=calcMeasures(indx_sort,corners,labels,measures,parameters);
   figure(1);clf
   set(gcf,'Position',[371 136 1238 825])
   measure=scale*measure;
   plot([0:15],measure);grid on
   set(gca,'FontSize',8)
   set(gca,'XTick',[0:15])
   set(gca,'XTickLabel',tickLabel)
   %rotateticklabel(gca,90);
   ylabel(yaxLabel)
   l=xlabel(xaxLabel);
   %set(l,'FontSize',[7])
   %set(l,'Position',[1 min(min(measure))])
   %set(l,'BackGroundColor',[1 1 1])
   l=legend(legendText,legLoc);
   set(l,'FontSize',6)
   l=title(sprintf('%s (%s)',strrep(spec,'_','\_'),strrep(exp,'_','\_')));
   set(l,'FontSize',7)
   %
   [ymin,imin]=min(measures);cmin=corners(imin,:);
   [ymax,imax]=max(measures);cmax=corners(imax,:);
   deltaVec=num2cell(deltas/max(deltas));
   deltaVec(indx_sort)=deltaVec;
   stats(it,:)=[spec yaxLabel {scale*ymin} {scale*mean(measures)} {scale*ymax} cmin cmax deltaVec];
   it=it+1;
   pause
   print(['plots/' exp '_' spec],'-dmeta')
   %
   export_fig(fileName_pdf,'-pdf','-transparent','-append','-nocrop')
end
header=['SPEC' 'UNITS' 'MINIMUM' 'AVERAGE' 'MAXIMUM' parameters parameters parameters];
xlswrite(['stats_' exp '.xls'],[header;stats])