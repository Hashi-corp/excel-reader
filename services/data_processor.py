import os
import matplotlib.pyplot as plt
import pandas as pd

def generate_and_save_plots(df: pd.DataFrame, plot_types: list, plots_dir: str) -> list:
    print(f"Requested plot types: {plot_types}")
    print(f"DataFrame columns: {df.columns.tolist()}")
    os.makedirs(plots_dir, exist_ok=True)
    plot_files = []
    # Normalize plot type names
    plot_type_map = {
        'bar': 'bar', 'bar chart': 'bar',
        'line': 'line', 'line chart': 'line',
        'scatter': 'scatter', 'scatter plot': 'scatter',
        'pie': 'pie', 'pie chart': 'pie',
        'histogram': 'hist', 'hist': 'hist', 'histogram plot': 'hist'
    }
    for plot_type in plot_types:
        normalized_type = plot_type_map.get(plot_type.strip().lower(), plot_type.strip().lower())
        print(f"Processing plot type: {plot_type} (normalized: {normalized_type})")
        fig, ax = plt.subplots()
        try:
            if normalized_type == 'bar':
                df.select_dtypes(include=['number']).plot(kind='bar', ax=ax)
            elif normalized_type == 'line':
                df.select_dtypes(include=['number']).plot(kind='line', ax=ax)
            elif normalized_type == 'scatter' and len(df.select_dtypes(include=['number']).columns) >= 2:
                cols = df.select_dtypes(include=['number']).columns[:2]
                df.plot.scatter(x=cols[0], y=cols[1], ax=ax)
            elif normalized_type == 'pie' and len(df.columns) >= 2:
                df.iloc[:,1].value_counts().plot.pie(ax=ax)
            elif normalized_type == 'hist':
                df.select_dtypes(include=['number']).plot(kind='hist', ax=ax)
            else:
                print(f"Skipping unsupported or unrecognized plot type: {normalized_type}")
                plt.close(fig)
                continue
            plot_path = os.path.join(plots_dir, f"plot_{normalized_type}.png")
            fig.savefig(plot_path)
            if not os.path.exists(plot_path):
                print(f"Failed to save plot: {plot_path}")
            else:
                print(f"Saved plot: {plot_path}")
                plot_files.append(plot_path)
        except Exception as e:
            print(f"Error generating {normalized_type} plot: {e}")
        finally:
            plt.close(fig)
    if not plot_files:
        raise RuntimeError("No plots were generated. Check your data and plot types.")
    return plot_files
