%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WARP
%
% Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D.
%   (2021). Algorithms for the automated correction of vertical drift
%   in eye-tracking data. Behavior Research Methods.
%
% https://doi.org/10.3758/s13428-021-01554-0
% https://github.com/jwcarr/drift
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = warp(fixation_XY, word_XY)

	n = size(fixation_XY, 1);
	[~, dtw_path] = dynamic_time_warping(fixation_XY, word_XY);
	for fixation_i = 1 : n
		words_mapped_to_fixation_i = cell2mat(dtw_path{fixation_i});
		candidate_Y = word_XY(words_mapped_to_fixation_i, 2);
		fixation_XY(fixation_i, 2) = mode(candidate_Y);
	end

end
