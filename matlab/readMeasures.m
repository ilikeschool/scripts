%
% function [corners,parameters,measures]=readMeasures(fileName,param_indxs,redIndx,redVar,spec);
%
% Reads contents of Excel file and outputs single measurement and independent variables
%
% fileName - Excel file name
% param_indxs - corner columns
% spec - measurement name
% redIndx (optional) - reduction measurement column
% redVar (optional) - value used for reduction
%
% corners - corner values
% parameters - corner names
% measures - measurements
%
function [corners,parameters,measures]=readMeasures(fileName,param_indxs,redIndx,redVar,spec);
%
[numeric,txt,raw]=xlsread(fileName);
%
corners=raw(2:end,param_indxs);
parameters=raw(1,param_indxs);
msr_indx=cellFind(raw(1,:),spec);
measures=cell2mat(raw(2:end,msr_indx));
if (isempty(redIndx))
else
   indx=cellFind(raw(2:end,redIndx),redVar);
   corners=corners(indx,:);
   measures=measures(indx);
end