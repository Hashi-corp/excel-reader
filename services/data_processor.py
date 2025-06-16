import os
import matplotlib.pyplot as plt
import pandas as pd

def generate_and_save_plots(df: pd.DataFrame, plot_types: list, plots_dir: str) -> list:
    """
    Generate plots based on plot_types and save them in plots_dir.
    Returns a list of file paths to the saved plots.
    """
    os.makedirs(plots_dir, exist_ok=True)
    plot_files = []
    for plot_type in plot_types:
        plot_type = plot_type.strip().lower()
        fig, ax = plt.subplots()
        if plot_type == 'bar':
            df.select_dtypes(include=['number']).plot(kind='bar', ax=ax)
        elif plot_type == 'line':
            df.select_dtypes(include=['number']).plot(kind='line', ax=ax)
        elif plot_type == 'scatter' and len(df.select_dtypes(include=['number']).columns) >= 2:
            cols = df.select_dtypes(include=['number']).columns[:2]
            df.plot.scatter(x=cols[0], y=cols[1], ax=ax)
        elif plot_type == 'pie' and len(df.columns) >= 2:
            df.iloc[:,1].value_counts().plot.pie(ax=ax)
        elif plot_type == 'histogram' or plot_type == 'hist':
            df.select_dtypes(include=['number']).plot(kind='hist', ax=ax)
        else:
            plt.close(fig)
            continue
        plot_path = os.path.join(plots_dir, f"plot_{plot_type}.png")
        fig.savefig(plot_path)
        plot_files.append(plot_path)
        plt.close(fig)
    return plot_files
