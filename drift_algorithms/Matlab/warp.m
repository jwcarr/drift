%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WARP
% The dynamic_time_warping function was adapted from:
% https://github.com/talcs/simpledtw
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = warp(fixation_XY, character_XY)

	n = size(fixation_XY, 1);
	warping_path = dynamic_time_warping(fixation_XY, character_XY);
	for fixation_i = 1 : n
		characters_mapped_to_fixation_i = cell2mat(warping_path{fixation_i});
		candidate_Y = character_XY(characters_mapped_to_fixation_i, 2);
		fixation_XY(fixation_i, 2) = mode(candidate_Y);
	end

end

function warping_path = dynamic_time_warping(sequence1, sequence2)

	n1 = size(sequence1, 1);
	n2 = size(sequence2, 1);
	cost_matrix = zeros(n1+1, n2+1);
	cost_matrix(1, :) = Inf;
	cost_matrix(:, 1) = Inf;
	cost_matrix(1, 1) = 0;
	for i = 1 : n1
		for j = 1 : n2
			cost = sqrt((sequence1(i,1) - sequence2(j,1))^2 + (sequence1(i,2) - sequence2(j,2))^2);
			cost_matrix(i+1, j+1) = cost + min([cost_matrix(i, j+1), cost_matrix(i+1, j), cost_matrix(i, j)]);
		end
	end
	cost_matrix = cost_matrix(2:n1+1, 2:n2+1);
	warping_path(1:n1) = {{}};
	while i > 1 || j > 1
		warping_path{i}{end+1} = j;
		possible_moves = [Inf, Inf, Inf];
		if i > 1 && j > 1
			possible_moves(1) = cost_matrix(i-1, j-1);
		end
		if i > 1
			possible_moves(2) = cost_matrix(i-1, j);
		end
		if j > 1
			possible_moves(3) = cost_matrix(i, j-1);
		end
		[~, best_move] = min(possible_moves);
		if best_move == 1
			i = i - 1;
			j = j - 1;
		elseif best_move == 2
			i = i - 1;
		else
			j = j - 1;
		end
	end
	warping_path{1}{end+1} = 1;

end
