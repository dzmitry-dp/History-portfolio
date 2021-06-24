from app.portfolio.calculations import get_plotting_dataframe


def draw_result_pips_graph(portfolio_data):
    df_for_plotting = get_plotting_dataframe(portfolio_data)
    plot = df_for_plotting.plot()
    fig = plot.get_figure()
    fig.savefig('app/static/img/result_pips.png')
