

def draw_result_pips_graph(df):
    plot = df.plot()
    fig = plot.get_figure()
    fig.savefig('app/static/img/result_pips.png')
