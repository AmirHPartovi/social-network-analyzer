# 📊 Social Graph Network Analyzer

A powerful **Streamlit** app for analyzing and comparing real-world social network graphs from `.txt` edge list files. It extracts deep structural statistics using **NetworkX** and provides **visualizations** and **Gephi-compatible exports**.

---

## 🚀 Features

- ✅ Upload multiple `.txt` files (edge list format)
- 📈 Comprehensive graph analysis for each file:
  - Degree statistics (average, max)
  - Centralities: Degree, Closeness, Betweenness, Eigenvector
  - Clustering Coefficient & Transitivity
  - Graph Density, Diameter, and Average Shortest Path Length
  - Graph Efficiency, Assortativity Coefficient
  - K-core decomposition
- 🔍 Comparative analysis across multiple networks
- 🎨 Visual preview of subgraphs (first 50 nodes)
- 📤 Export graphs in `.gml` format for **Gephi**

---

## 📁 Input Format

Each graph should be uploaded as a plain `.txt` file in **edge list** format:

1 2 2 3 3 4
Each line represents a connection between two nodes.

---

## 🛠 Installation & Running

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Install dependencies:

```bash
streamlit run graph_analysis_app.py
```

📤 Output
📄 .gml file downloads for visual analysis in Gephi

📊 Table and chart comparisons between uploaded graphs

🖼 Network graph visualization using NetworkX

🧪 Sample Datasets
For testing, try real-world datasets like:

Facebook Social Circles

Twitter Ego Networks

SNAP Graphs: https://snap.stanford.edu/data/

📦 Dependencies
Python 3.8+

Streamlit

NetworkX

Pandas

Matplotlib

🤝 Contributing
Contributions are welcome! Feel free to fork the repo, suggest improvements, or submit pull requests.

👨‍💻 Developer
Amir Hossein Partovi
📧 a.partovi99@gmail.com

📄 License
MIT License
