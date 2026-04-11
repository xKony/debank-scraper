import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import io
import glob
from config import GRAPHS_DIR, SAVE_GRAPHS
from logger import get_logger

log = get_logger(__name__)

def get_latest_csv():
    """Finds the newest portfolio_*.csv file in results/csv/."""
    files = glob.glob(os.path.join("results", "csv", "portfolio_*.csv"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def parse_multi_csv(file_path):
    """Parses the multi-section CSV file into a dictionary of DataFrames."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    current_section = None
    section_data = []
    
    for line in content.splitlines():
        line = line.strip()
        if not line:
            if current_section and section_data:
                sections[current_section] = "\n".join(section_data)
                section_data = []
                current_section = None
            continue
            
        # Detect section headers
        if line in ["Total Balance", "Chain", "Project"]:
            current_section = line
            continue
            
        if current_section:
            section_data.append(line)
            
    # Final section
    if current_section and section_data:
        sections[current_section] = "\n".join(section_data)
        
    dfs = {}
    for name, data in sections.items():
        try:
            dfs[name] = pd.read_csv(io.StringIO(data))
        except Exception as e:
            log.error(f"Error parsing section {name}: {e}")
            
    return dfs

def generate_graphs(show_graphs=False):
    """Main function to generate and save/show graphs."""
    latest_csv = get_latest_csv()
    if not latest_csv:
        log.warning("No portfolio CSV files found in results/csv/ to generate graphs.")
        return

    log.info(f"Generating graphs from: {latest_csv}")
    dfs = parse_multi_csv(latest_csv)
    
    if not dfs:
        log.error("Could not parse any data sections from the CSV.")
        return

    # Ensure graphs directory exists
    if not os.path.exists(GRAPHS_DIR):
        os.makedirs(GRAPHS_DIR)
        log.info(f"Created directory: {GRAPHS_DIR}")

    sns.set_theme(style="whitegrid")

    # 1. Total Balance Distribution
    if "Total Balance" in dfs:
        df_total = dfs["Total Balance"]
        if "Total USD Value" in df_total.columns:
            plt.figure(figsize=(10, 6))
            
            # Subplot 1: Histogram
            plt.subplot(1, 2, 1)
            sns.histplot(df_total["Total USD Value"], kde=True, color="skyblue")
            plt.title("Total Balance Distribution (Histogram)")
            plt.xlabel("USD Value")
            
            # Subplot 2: Boxplot
            plt.subplot(1, 2, 2)
            sns.boxplot(y=df_total["Total USD Value"], color="lightgreen")
            plt.title("Total Balance Distribution (Boxplot)")
            plt.ylabel("USD Value")
            
            plt.tight_layout()
            if SAVE_GRAPHS:
                plt.savefig(os.path.join(GRAPHS_DIR, "total_balance_dist.png"))
            if show_graphs:
                plt.show(block=False)

    # 2. Chain Value Distribution
    if "Chain" in dfs:
        df_chain = dfs["Chain"]
        # Melt to get long format: Wallet Address, Chain, Value
        df_melted = df_chain.melt(id_vars=["Wallet Address"], var_name="Chain", value_name="Value")
        # Sum by chain
        chain_totals = df_melted.groupby("Chain")["Value"].sum().sort_values(ascending=False).reset_index()
        # Top 15 chains
        top_chains = chain_totals.head(15)
        
        if not top_chains.empty:
            plt.figure(figsize=(12, 6))
            sns.barplot(data=top_chains, x="Value", y="Chain", hue="Chain", palette="viridis", legend=False)
            plt.title("Top 15 Chains by Total USD Value")
            plt.xlabel("Total USD Value")
            plt.ylabel("Chain Name")
            
            plt.tight_layout()
            if SAVE_GRAPHS:
                plt.savefig(os.path.join(GRAPHS_DIR, "top_chains.png"))
            if show_graphs:
                plt.show(block=False)

    # 3. Project Value Distribution
    if "Project" in dfs:
        df_proj = dfs["Project"]
        df_melted_proj = df_proj.melt(id_vars=["Wallet Address"], var_name="Project", value_name="Value")
        proj_totals = df_melted_proj.groupby("Project")["Value"].sum().sort_values(ascending=False).reset_index()
        top_projs = proj_totals.head(15)
        
        if not top_projs.empty:
            plt.figure(figsize=(12, 6))
            sns.barplot(data=top_projs, x="Value", y="Project", hue="Project", palette="magma", legend=False)
            plt.title("Top 15 Projects by Total USD Value")
            plt.xlabel("Total USD Value")
            plt.ylabel("Project Name")
            
            plt.tight_layout()
            if SAVE_GRAPHS:
                plt.savefig(os.path.join(GRAPHS_DIR, "top_projects.png"))
            if show_graphs:
                plt.show() # Last one can block if interactive
            else:
                plt.close('all')

    log.info(f"Graphs successfully saved to {GRAPHS_DIR}")

if __name__ == "__main__":
    generate_graphs(show_graphs=False)
