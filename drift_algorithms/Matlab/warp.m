%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WARP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = warp(fixation_XY, character_XY)

	n = size(fixation_XY, 1);
	[~, dtw_path] = dynamic_time_warping(fixation_XY, character_XY);
	for fixation_i = 1 : n
		characters_mapped_to_fixation_i = cell2mat(dtw_path{fixation_i});
		candidate_Y = character_XY(characters_mapped_to_fixation_i, 2);
		fixation_XY(fixation_i, 2) = mode(candidate_Y);
	end

end
