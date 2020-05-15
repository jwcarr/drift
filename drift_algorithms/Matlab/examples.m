% For Octave compatibility, first load the statistics package
if exist('OCTAVE_VERSION')
	pkg load statistics
end

% Matrix representing the XY coordinates of the original fixations
fixation_XY = [395, 150; 479, 152; 619, 155; 670, 168; 726, 142; 912, 161; 1086, 176; 401, 212; 513, 230; 594, 228; 725, 229; 806, 231; 884, 216; 1000, 234; 1133, 225; 379, 270; 472, 273; 645, 310; 713, 289; 788, 288; 948, 286; 1072, 307; 378, 360; 496, 357; 634, 338];

% Vector representing the Y coordinates of the lines of text
line_Y = [155, 219, 283, 347];

% Matrix representing the XY coordinates of the characters of text (only needed by warp)
character_XY = [368, 155; 384, 155; 400, 155; 416, 155; 432, 155; 464, 155; 480, 155; 496, 155; 512, 155; 528, 155; 560, 155; 576, 155; 592, 155; 608, 155; 624, 155; 656, 155; 672, 155; 688, 155; 720, 155; 736, 155; 752, 155; 768, 155; 816, 155; 832, 155; 848, 155; 864, 155; 880, 155; 896, 155; 912, 155; 928, 155; 944, 155; 960, 155; 976, 155; 1008, 155; 1024, 155; 1040, 155; 1056, 155; 1072, 155; 1088, 155; 1104, 155; 1120, 155; 1136, 155; 1152, 155; 368, 219; 384, 219; 400, 219; 416, 219; 464, 219; 480, 219; 496, 219; 512, 219; 528, 219; 560, 219; 576, 219; 592, 219; 608, 219; 624, 219; 656, 219; 672, 219; 688, 219; 704, 219; 720, 219; 736, 219; 752, 219; 784, 219; 800, 219; 816, 219; 832, 219; 880, 219; 896, 219; 912, 219; 944, 219; 960, 219; 976, 219; 992, 219; 1008, 219; 1024, 219; 1040, 219; 1056, 219; 1088, 219; 1104, 219; 1120, 219; 1136, 219; 1152, 219; 368, 283; 384, 283; 400, 283; 432, 283; 448, 283; 464, 283; 480, 283; 496, 283; 512, 283; 528, 283; 544, 283; 560, 283; 608, 283; 624, 283; 640, 283; 656, 283; 672, 283; 704, 283; 720, 283; 736, 283; 768, 283; 784, 283; 800, 283; 816, 283; 832, 283; 848, 283; 864, 283; 880, 283; 912, 283; 928, 283; 944, 283; 960, 283; 976, 283; 992, 283; 1040, 283; 1056, 283; 1072, 283; 1088, 283; 1104, 283; 368, 347; 384, 347; 400, 347; 416, 347; 432, 347; 464, 347; 480, 347; 496, 347; 512, 347; 528, 347; 544, 347; 576, 347; 592, 347; 608, 347; 624, 347; 640, 347; 656, 347];

% Matrix representing the XY coordinate of the centers of the words (only needed by matchup)
word_XY = word_XY = [400, 155; 496, 155; 592, 155; 672, 155; 744, 155; 896, 155; 1080, 155; 392, 219; 496, 219; 592, 219; 704, 219; 808, 219; 896, 219; 1000, 219; 1120, 219; 384, 283; 496, 283; 640, 283; 720, 283; 824, 283; 952, 283; 1072, 283; 400, 347; 504, 347; 616, 347];

disp('Original fixation sequence');
disp(fixation_XY);

attach_output = attach(fixation_XY, line_Y);
disp('Output from the attach algorithm');
disp(attach_output);

chain_output = chain(fixation_XY, line_Y);
disp('Output from the chain algorithm');
disp(chain_output);

cluster_output = cluster(fixation_XY, line_Y);
disp('Output from the cluster algorithm');
disp(cluster_output);

matchup_output = matchup(fixation_XY, line_Y, word_XY);
disp('Output from the matchup algorithm');
disp(matchup_output);

regress_output = regress(fixation_XY, line_Y);
disp('Output from the regress algorithm');
disp(regress_output);

segment_output = segment(fixation_XY, line_Y);
disp('Output from the segment algorithm');
disp(segment_output);

warp_output = warp(fixation_XY, character_XY);
disp('Output from the warp algorithm');
disp(warp_output);
