"""Social media network analysis tool using streamlit."""
import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import io
import tempfile

st.set_page_config(page_title="Social Graph Analyzer")
st.title("📊 Social Graph Network Analyzer")
st.write(
    "Upload your social network graph files (edge list format) to analyze various metrics and visualize the graphs.")
st.write(
    "This tool supports multiple file uploads and provides a comparison of different graphs.")
st.write(
    "You can also download the processed graph in GML format for further analysis in Gephi or other tools.")

uploaded_files = st.file_uploader(
    "📂 Upload Graph Files (edge list - txt)", type="txt", accept_multiple_files=True)

if uploaded_files:
    all_stats = []
    total_files = len(uploaded_files)

    # Add progress bar
    progress_bar = st.progress(0)

    for idx, uploaded_file in enumerate(uploaded_files):
        file_name = uploaded_file.name

        # Add spinner for each file
        with st.spinner(f'Processing file {idx + 1}/{total_files}: {file_name}...'):
            st.subheader(f"📁 File: {file_name}")

            # Load graph from uploaded file
            G = nx.read_edgelist(
                uploaded_file, create_using=nx.Graph(), nodetype=int)

            if not nx.is_connected(G):
                G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

            degs = [d for _, d in G.degree()]
            deg_centrality = nx.degree_centrality(G)
            cls_centrality = nx.closeness_centrality(G)
            btw_centrality = nx.betweenness_centrality(G, k=500)
            try:
                eigen = nx.eigenvector_centrality(G, max_iter=1000)
            except:
                eigen = {n: 0 for n in G.nodes()}

            stats = {
                "Nodes": G.number_of_nodes(),
                "Edges": G.number_of_edges(),
                "Avg Degree": sum(degs)/len(degs),
                "Max Degree": max(degs),
                "Clustering Coef": nx.average_clustering(G),
                "Density": nx.density(G),
                "Diameter": nx.diameter(G),
                "Avg Path Length": nx.average_shortest_path_length(G),
                "Transitivity": nx.transitivity(G),
                "Assortativity": nx.degree_assortativity_coefficient(G),
                "Graph Efficiency": nx.global_efficiency(G),
                "Avg Degree Centrality": sum(deg_centrality.values()) / len(deg_centrality),
                "Avg Closeness Centrality": sum(cls_centrality.values()) / len(cls_centrality),
                "Avg Betweenness Centrality": sum(btw_centrality.values()) / len(btw_centrality),
                "Avg Eigenvector Centrality": sum(eigen.values()) / len(eigen),
                "K-core Nodes": nx.k_core(G).number_of_nodes()
            }

            df_stats = pd.DataFrame(stats.items(), columns=["Metric", "Value"])
            st.dataframe(df_stats, use_container_width=True)

            # Display graph as a subset of first 50 nodes
            st.write("📌 Sample Graph Visualization (First 50 Nodes):")
            subgraph = G.subgraph(list(G.nodes())[:50])
            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(subgraph, ax=ax, node_size=50,
                    edge_color='gray', with_labels=False)
            st.pyplot(fig)

            # Save output for Gephi
            with tempfile.NamedTemporaryFile(delete=False, suffix=".gml") as tmp_file:
                nx.write_gml(G, tmp_file.name)
                st.download_button(
                    label="⬇️ Download GML Output for Gephi",
                    data=open(tmp_file.name, "rb").read(),
                    file_name=file_name.replace(".txt", ".gml"),
                    mime="application/octet-stream"
                )

            all_stats.append((file_name, stats))

            # Update progress bar
            progress = (idx + 1) / total_files
            progress_bar.progress(progress)

    # Clear progress bar when done
    progress_bar.empty()
    st.success('All files processed successfully! 🎉')

    # Compare graphs if multiple files are uploaded
    if len(all_stats) > 1:
        st.subheader("📊 Graph Comparison")
        compare_df = pd.DataFrame([s[1] for s in all_stats], index=[
            s[0] for s in all_stats])
        st.dataframe(compare_df, use_container_width=True)

        selected_metrics = st.multiselect("Select metrics for graphical comparison:",
                                          compare_df.columns.tolist(),
                                          default=["Avg Degree", "Clustering Coef"])

        if selected_metrics:
            st.bar_chart(compare_df[selected_metrics])
