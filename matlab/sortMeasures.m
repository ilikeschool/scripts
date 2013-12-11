%
% function [deltas,indx_sort]=sortMeasures(measures,corners);
%
% Calculates sensitivity of measurement to independent variables.  Assumes that corners are in
% ascending binary order.
%
% measures - measurements
% corners - corner values
%
% deltas - measurement sensitivity
% indx_sort - sensitivity indexes (sorted)
%
function [deltas,indx_sort]=sortMeasures(measures,corners);
%
[rows,cols]=size(corners);
v=[1:length(measures)];
for i=1:cols
   v2=[];
   for j=1:2^(cols-i+1)
      start=(j-1)*2^(i-1)+1;
      stop=(j)*2^(i-1);
      v2(j,:)=v(start:stop);
   end
   v3=reshape(v2,2,length(measures)/2);
   delta=measures(v3(2,:))-measures(v3(1,:));
   delta_measure(i)=mean(delta);
end
%
[deltas,indx_sort]=sort(abs(delta_measure),'descend');
indx_sort=cols-indx_sort+1;