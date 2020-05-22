%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% VandM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = VandM(fixation_XY, line_Y, sd_thresh)

	if ~exist('sd_thresh', 'var')
		sd_thresh = 2;
	end

	n = size(fixation_XY, 1);
	diff_X = diff(fixation_XY(:, 1));
	x_thresh = median(diff_X) - sd_thresh * std(diff_X);
	end_line_indices = find(diff_X < x_thresh).';
	end_line_indices = [end_line_indices, n];
	start_of_line = 1;
	for end_of_line = end_line_indices
		mean_y = mean(fixation_XY(start_of_line:end_of_line, 2));
		[~, line_i] = min(abs(line_Y - mean_y));
		fixation_XY(start_of_line:end_of_line, 2) = line_Y(line_i);
		start_of_line = end_of_line + 1;
	end

end
