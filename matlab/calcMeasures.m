%
% function [measure,tickLabel,xaxLabel,legendText]=calcMeasures(indx_sort,corners,labels,measures,parameters);
%
% Creates data for plotting.  Currently supports 6-8 independent variables. X axis is 4 variables, remaining variables
% used to generate family of curves.
%
% measure - 4xN matrix of measures to plot
% tickLabel - x axis tick labels
% xaxLabel - x axis label
% legendText - curve family legend text
%
% indx_sort - sensitivity indexes (sorted)
% corners - corner values
% labels - corner value labels
% measures - measurements
% parameters - corner names
%
function [measure,tickLabel,xaxLabel,legendText]=calcMeasures(indx_sort,corners,labels,measures,parameters);
%
coli=indx_sort(1);
colj=indx_sort(2);
colk=indx_sort(3);
coll=indx_sort(4);
it=1;
for i=1:2
   for j=1:2
      for k=1:2
         for l=1:2
            indx_i=cellFind(corners(:,coli),labels(i,coli));
            indx_j=cellFind(corners(indx_i,colj),labels(j,colj));
            indx_k=cellFind(corners(indx_i(indx_j),colk),labels(k,colk));
            indx_l=cellFind(corners(indx_i(indx_j(indx_k)),coll),labels(l,coll));
            indx=indx_i(indx_j(indx_k(indx_l)));
            measure(it,:)=measures(indx);
            tickLabel{it}=cell2mat([labels(i,coli) '/' labels(j,colj) '/' labels(k,colk) '/' labels(l,coll)]);
            it=it+1;
         end
      end
   end
end
%
xaxLabel=[parameters(indx_sort(1))];
for i=2:4
   xaxLabel=[xaxLabel ' / ' parameters(indx_sort(i))];
end
xaxLabel=cell2mat(xaxLabel);
%
indx_sort=sort(indx_sort(5:end));
coli=indx_sort(1);
colj=indx_sort(2);
if (length(indx_sort)>2)
   colk=indx_sort(3);
end
if (length(indx_sort)>3)
   coll=indx_sort(4);
end
it=1;
if (length(indx_sort)==4)
   for i=1:2
      for j=1:2
         for k=1:2
            for l=1:2
               legendText{it}=[parameters{coli} '=' labels{i,coli} ', ' ...
                               parameters{colj} '=' labels{j,colj} ', ' ...
                               parameters{colk} '=' labels{k,colk} ', ' ...
                               parameters{coll} '=' labels{l,coll}];
               it=it+1;
            end
         end
      end
   end
elseif (length(indx_sort)==3)
   for i=1:2
      for j=1:2
         for k=1:2
            legendText{it}=[parameters{coli} '=' labels{i,coli} ', ' ...
                            parameters{colj} '=' labels{j,colj} ', ' ...
                            parameters{colk} '=' labels{k,colk}];
            it=it+1;
         end
      end
   end
else
    for i=1:2
      for j=1:2
            legendText{it}=[parameters{coli} '=' labels{i,coli} ', ' ...
                            parameters{colj} '=' labels{j,colj}];
            it=it+1;
         end
      end
   end
end