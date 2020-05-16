%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MATCHUP
% This is an implementation of the method reported in:
% Lima Sanches, C., Kise, K., & Augereau, O. (2015). Eye gaze and text
%   line matching for reading analysis. In Adjunct proceedings of the
%   2015 ACM International Joint Conference on Pervasive and
%   Ubiquitous Computing and proceedings of the 2015 ACM International
%   Symposium on Wearable Computers (pp. 1227–1233). New York, NY:
%   Association for Computing Machinery. doi:10.1145/2800835.2807936
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = matchup(fixation_XY, word_XY, x_thresh)

	if ~exist('x_thresh')
		x_thresh = 512;
	end

	line_Y = unique(word_XY(:, 2));
	n = size(fixation_XY, 1);
	m = length(line_Y);
	diff_X = diff(fixation_XY(:, 1));
	end_line_indices = find(diff_X < -x_thresh).';
	end_line_indices = [end_line_indices, n];
	start_of_line = 1;
	for end_of_line = end_line_indices
		gaze_line = fixation_XY(start_of_line:end_of_line, :);
		line_costs = zeros(1, m);
		for candidate_line_i = 1 : m
			text_line = word_XY(word_XY(:, 2) == line_Y(candidate_line_i), :);
			dtw_cost = dynamic_time_warping(gaze_line, text_line);
			line_costs(candidate_line_i) = dtw_cost;
		end
		[~, line_i] = min(line_costs);
		fixation_XY(start_of_line:end_of_line, 2) = line_Y(line_i);
		start_of_line = end_of_line + 1;
	end

end
