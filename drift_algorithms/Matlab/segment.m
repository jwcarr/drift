function fixation_XY = segment(fixation_XY, line_Y)

	n = size(fixation_XY, 1);
	m = length(line_Y);
	diff_X = diff(fixation_XY(:, 1));
	[_, saccades_ordered_by_length] = sort(diff_X);
	line_change_indices = saccades_ordered_by_length(1:m-1);
	current_line_i = 1;
	for fixation_i = 1 : n
		fixation_XY(fixation_i, 2) = line_Y(current_line_i);
		if ismember(fixation_i, line_change_indices)
			current_line_i = current_line_i + 1;
		end
	end

end
