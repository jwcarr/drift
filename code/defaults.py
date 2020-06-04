y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

colors = {'attach':'#81818D',
          'chain':'#D64E7A',
          'cluster':'#45ADEC',
          'compare':'#F3711A',
          'merge':'#205E84',
          'regress':'#009142',
          'segment':'#FCAF32',
          'split':'#E32823',
          'warp':'#6742B0',
          'gold':'#B0944B',
          'JC':'black',
          'VP':'black'
}

algorithms = ['attach', 'chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'warp']

true_algorithms = ['chain', 'cluster', 'compare', 'merge', 'regress', 'segment', 'split', 'warp']

good_algorithms = ['attach', 'chain', 'cluster', 'merge', 'regress', 'segment', 'split', 'warp']

factors = {'noise':('Noise distortion', (0, 40)),
           'slope':('Slope distortion', (-0.1, 0.1)),
           'shift':('Shift distortion', (-0.2, 0.2)),
           'regression_within':('Probability of within-line regression', (0, 1)),
           'regression_between':('Probability of between-line regression', (0, 1))}
