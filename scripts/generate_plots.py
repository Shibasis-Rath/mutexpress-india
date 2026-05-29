import pandas as pd
import plotly.express as px

print("Loading integrated results...")
df = pd.read_csv("../results/mutexpress_india_output.csv")

print("Generating Priority Distribution Pie Chart...")
counts = df["MutExpress_Priority"].value_counts().reset_index()
counts.columns = ["Priority", "Count"]

fig = px.pie(counts, names="Priority", values="Count",
             title="MutExpress-India: Gene Priority Distribution",
             color="Priority",
             color_discrete_map={
                 "HIGH": "#E63946", "MEDIUM_V": "#F4A261",
                 "MEDIUM_E": "#457B9D", "LOW": "#A8DADC"
             })
fig.write_html("../results/priority_pie.html")
print("Saved: results/priority_pie.html")

print("Generating HIGH Priority Scatter Plot...")
# Filter for HIGH priority and ensure we don't have empty data
high = df[df["MutExpress_Priority"] == "HIGH"].dropna(subset=["log2FoldChange", "damage_score"]).copy()

fig2 = px.scatter(high,
    x="log2FoldChange", y="damage_score",
    hover_name="gene", color="direction",
    color_discrete_map={"UP": "#E63946", "DOWN": "#457B9D"},
    title="HIGH Priority Genes: Expression Change vs Variant Severity",
    labels={"log2FoldChange": "Log2 Fold Change (Tumor/Normal)",
            "damage_score": "Damage Score (1-3)"}
)
fig2.add_vline(x=0, line_dash="dash", line_color="grey")
fig2.write_html("../results/high_priority_scatter.html")
print("Saved: results/high_priority_scatter.html")

print("\nPhase 4 (Part 1) Complete! Plots generated successfully.")
