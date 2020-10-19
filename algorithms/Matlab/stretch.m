%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% STRETCH
%
% Lohmeier, S. (2015). Experimental evaluation and modelling of the
%   comprehension of indirect anaphors in a programming language
%   (Master’s thesis). Technische Universität Berlin.
%
% http://www.monochromata.de/master_thesis/ma1.3.pdf
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function fixation_XY = stretch(fixation_XY, line_Y, scale_bounds, offset_bounds)

	if ~exist('scale_bounds', 'var')
		scale_bounds = [0.9, 1.1];
	end
	if ~exist('offset_bounds', 'var')
		offset_bounds = [-50, 50];
	end

	n = size(fixation_XY, 1);
	fixation_Y = fixation_XY(:, 2).';

	function [alignment_error, corrected_Y] = fit_lines(params)
		candidate_Y = fixation_Y * params(1) + params(2);
		corrected_Y = zeros(1, n);
		for fixation_i = 1 : n
			[~, line_i] = min(abs(line_Y - candidate_Y(fixation_i)));
			corrected_Y(fixation_i) = line_Y(line_i);
		end
		alignment_error = sum(abs(candidate_Y - corrected_Y));
	end

	lower_bounds = [scale_bounds(1), offset_bounds(1)];
	upper_bounds = [scale_bounds(2), offset_bounds(2)];
	best_fit = fminsearchbnd(@fit_lines, [1, 0], lower_bounds, upper_bounds); % Octave < 6.0 does not support handles to nested functions
	[~, correction] = fit_lines(best_fit);
	fixation_XY(:, 2) = correction;

end
