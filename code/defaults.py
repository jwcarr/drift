y_to_line_mapping = {155:1, 219:2, 283:3, 347:4, 411:5, 475:6, 539:7, 603:8, 667:9, 731:10, 795:11, 859:12, 923:13}

colors = {'attach':'#6B6B7F',
          'chain':'#E85A71',
          'cluster':'#4EA1D3',
          'matchup':'#E0782A',
          'regress':'#FCBE32',
          'segment':'#17A363',
          'warp':'#7544D6',
          'gold':'#B0944B',
          'JC':'black',
          'VP':'black'
}

algorithms = ['attach', 'chain', 'cluster', 'matchup', 'regress', 'segment', 'warp']

true_algorithms = ['chain', 'cluster', 'matchup', 'regress', 'segment', 'warp']

algorithms_plus_gold = ['attach', 'chain', 'cluster', 'matchup', 'regress', 'segment', 'warp', 'gold']

factors = {'noise':('Noise distortion', (0, 40)),
           'slope':('Slope distortion', (-0.1, 0.1)),
           'shift':('Shift distortion', (-0.2, 0.2)),
           'regression_within':('Within-line regression', (0, 1)),
           'regression_between':('Between-line regression', (0, 1))}