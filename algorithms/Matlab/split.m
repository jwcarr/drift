%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SPLIT
%
% Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D.
%   (2021). Algorithms for the automated correction of vertical drift
%   in eye tracking data. Behavior Research Methods.
%
% https://doi.org/10.3758/s13428-021-01554-0
% https://github.com/jwcarr/drift
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = split(fixation_XY, line_Y)

	n = size(fixation_XY, 1);
	diff_X = diff(fixation_XY(:, 1));
	[clusters, centers] = kmeans(diff_X, 2, 'Replicates', 10, 'MaxIter', 300);
	[~, sweep_marker] = min(centers);
	end_line_indices = find(clusters == sweep_marker).';
	end_line_indices = [end_line_indices, n];
	start_of_line = 1;
	for end_of_line = end_line_indices
		mean_y = mean(fixation_XY(start_of_line:end_of_line, 2));
		[~, line_i] = min(abs(line_Y - mean_y));
		fixation_XY(start_of_line:end_of_line, 2) = line_Y(line_i);
		start_of_line = end_of_line + 1;
	end

end
