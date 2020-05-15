import numpy as np
from sklearn.cluster import KMeans
from scipy.optimize import minimize
from scipy.stats import norm

def correct_drift(method, fixation_XY, passage):
	if method == 'attach':
		return attach(fixation_XY, passage.line_positions)
	elif method == 'chain':
		return chain(fixation_XY, passage.line_positions)
	elif method == 'cluster':
		return cluster(fixation_XY, passage.line_positions)
	elif method == 'matchup':
		return matchup(fixation_XY, passage.line_positions, passage.word_centers())
	elif method == 'regress':
		return regress(fixation_XY, passage.line_positions)
	elif method == 'segment':
		return segment(fixation_XY, passage.line_positions)
	elif method == 'warp':
		return warp(fixation_XY, passage.char_xy)
	else:
		raise ValueError('Invalid method')

def attach(fixation_XY, line_Y):
	n = len(fixation_XY)
	for fixation_i in range(n):
		line_i = np.argmin(abs(line_Y - fixation_XY[fixation_i, 1]))
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

def chain(fixation_XY, line_Y, x_thresh=192, y_thresh=32):
	n = len(fixation_XY)
	dist_X = abs(np.diff(fixation_XY[:, 0]))
	dist_Y = abs(np.diff(fixation_XY[:, 1]))
	end_chain_indices = list(np.where(np.logical_or(dist_X > x_thresh, dist_Y > y_thresh))[0] + 1)
	end_chain_indices.append(n)
	start_of_chain = 0
	for end_of_chain in end_chain_indices:
		mean_y = np.mean(fixation_XY[start_of_chain:end_of_chain, 1])
		line_i = np.argmin(abs(line_Y - mean_y))
		fixation_XY[start_of_chain:end_of_chain, 1] = line_Y[line_i]
		start_of_chain = end_of_chain
	return fixation_XY

def cluster(fixation_XY, line_Y):
	m = len(line_Y)
	fixation_Y = fixation_XY[:, 1].reshape(-1, 1)
	clusters = KMeans(m).fit_predict(fixation_Y)
	centers = [fixation_Y[clusters == i].mean() for i in range(m)]
	ordered_cluster_indices = np.argsort(centers)
	for fixation_i, cluster_i in enumerate(clusters):
		line_i = np.where(ordered_cluster_indices == cluster_i)[0][0]
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

def matchup(fixation_XY, line_Y, word_XY, x_thresh=512):
	n = len(fixation_XY)
	diff_X = np.diff(fixation_XY[:, 0])
	end_line_indices = list(np.where(diff_X < -x_thresh)[0] + 1)
	end_line_indices.append(n)
	text_lines = [word_XY[np.where(word_XY[:, 1] == line_y)] for line_y in line_Y]
	start_line_index = 0
	for end_line_index in end_line_indices:
		gaze_line = fixation_XY[start_line_index:end_line_index]
		line_costs = [dynamic_time_warping(gaze_line, text_line)[0] for text_line in text_lines]
		line_i = np.argmin(line_costs)
		fixation_XY[start_line_index:end_line_index, 1] = line_Y[line_i]
		start_line_index = end_line_index
	return fixation_XY

def regress(fixation_XY, line_Y, k_bounds=(-0.1, 0.1), o_bounds=(-50, 50), s_bounds=(1, 20)):
	n = len(fixation_XY)
	m = len(line_Y)

	def fit_lines(params, return_line_assignments=False):
		k = k_bounds[0] + (k_bounds[1] - k_bounds[0]) * norm.cdf(params[0])
		o = o_bounds[0] + (o_bounds[1] - o_bounds[0]) * norm.cdf(params[1])
		s = s_bounds[0] + (s_bounds[1] - s_bounds[0]) * norm.cdf(params[2])
		predicted_Y_from_slope = fixation_XY[:, 0] * k
		line_Y_plus_offset = line_Y + o
		density = np.zeros((n, m))
		for line_i in range(m):
			fit_Y = predicted_Y_from_slope + line_Y_plus_offset[line_i]
			density[:, line_i] = norm.logpdf(fixation_XY[:, 1], fit_Y, s)
		if return_line_assignments:
			return density.argmax(axis=1)
		return -sum(density.max(axis=1))

	best_fit = minimize(fit_lines, [0, 0, 0], method='powell')
	line_assignments = fit_lines(best_fit.x, True)
	for fixation_i, line_i in enumerate(line_assignments):
		fixation_XY[fixation_i, 1] = line_Y[line_i]
	return fixation_XY

def segment(fixation_XY, line_Y):
	n = len(fixation_XY)
	m = len(line_Y)
	diff_X = np.diff(fixation_XY[:, 0])
	saccades_ordered_by_length = np.argsort(diff_X)
	line_change_indices = saccades_ordered_by_length[:m-1]
	current_line_i = 0
	for fixation_i in range(n):
		fixation_XY[fixation_i, 1] = line_Y[current_line_i]
		if fixation_i in line_change_indices:
			current_line_i += 1
	return fixation_XY

def warp(fixation_XY, character_XY):
	_, warping_path = dynamic_time_warping(fixation_XY, character_XY)
	for fixation_i, characters_mapped_to_fixation_i in enumerate(warping_path):
		candidate_Y = character_XY[characters_mapped_to_fixation_i, 1]
		fixation_XY[fixation_i, 1] = mode(candidate_Y)
	return fixation_XY

def mode(values):
	values = list(values)
	return max(set(values), key=values.count)

def dynamic_time_warping(sequence1, sequence2):
	n1 = len(sequence1)
	n2 = len(sequence2)
	dtw_cost = np.zeros((n1+1, n2+1))
	dtw_cost[0, :] = np.inf
	dtw_cost[:, 0] = np.inf
	dtw_cost[0, 0] = 0
	for i in range(n1):
		for j in range(n2):
			this_cost = np.sqrt(sum((sequence1[i] - sequence2[j])**2))
			dtw_cost[i+1, j+1] = this_cost + min(dtw_cost[i, j+1], dtw_cost[i+1, j], dtw_cost[i, j])
	dtw_cost = dtw_cost[1:, 1:]
	dtw_path = [[] for _ in range(n1)]
	while i > 0 or j > 0:
		dtw_path[i].append(j)
		possible_moves = [np.inf, np.inf, np.inf]
		if i > 0 and j > 0:
			possible_moves[0] = dtw_cost[i-1, j-1]
		if i > 0:
			possible_moves[1] = dtw_cost[i-1, j]
		if j > 0:
			possible_moves[2] = dtw_cost[i, j-1]
		best_move = np.argmin(possible_moves)
		if best_move == 0:
			i -= 1
			j -= 1
		elif best_move == 1:
			i -= 1
		else:
			j -= 1
	dtw_path[0].append(0)
	return dtw_cost[-1, -1], dtw_path
