# AlthenaXavier 

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyPI Version](https://img.shields.io/badge/pypi-3.0.0-blue)](https://pypi.org/project/althenaxavier)

**Industrial-grade AI-powered Big Data Processing Engine for Large CSV Files**

##  Features

-  **High-performance CSV processing** - Process GB-sized files with low memory
-  **AI-powered analytics** - Anomaly detection, trend analysis, forecasting
-  **Multi-file support** - Process multiple files with pattern matching
-  **Command Line Interface** - Easy to use CLI tool
-  **Adaptive chunk processing** - Auto-adjusts based on RAM
-  **Statistical analysis** - Mean, median, std deviation, quartiles
-  **Machine learning integration** - Isolation Forest, K-Means, Linear Regression

##  Installation

```bash
# Basic installation
pip install althenaxavier

# Full installation with all dependencies
pip install althenaxavier[full]


📌 Overview

AlthenaXavier is a lightweight, AI-powered data processing engine designed to handle large-scale CSV/Parquet datasets efficiently using chunk-based processing.

It combines data engineering + AI analytics into a single tool, making it suitable for preprocessing datasets up to 10GB+ on a single machine.

---

Key Features

Data Processing

- Chunk-based large file handling (memory-efficient)
- Multi-file processing support ("*.csv" patterns)
- Supports CSV, JSON, Excel, Parquet
- CLI-based execution

AI Capabilities

- Anomaly Detection (Isolation Forest)
- Forecasting (Linear Regression)
- Clustering (K-Means)
- Trend Analysis (Moving Average)

Smart Optimization

- Adaptive chunk size (based on system RAM)
- CPU-aware configuration
- Efficient column-level processing

---

Installation

pip install althenaxavier

Or clone manually:

git clone https://github.com/ARULGNANAKUMAR/althenaxavier.git
cd althenaxavier
pip install -r requirements.txt

---

Usage

 Process Single File

althenaxavier process data.csv --op sum --column sales

---

Process Multiple Files

althenaxavier process "data/*.csv" --op mean --column price

---

AI Analysis

althenaxavier ai data.csv --column revenue --analyze all

---

Compare Files

althenaxavier compare file1.csv file2.csv --column profit

---

🔹 Forecast

althenaxavier forecast sales.csv --column revenue --periods 30

---

Example Use Cases

- AI/ML Data Preprocessing
- Large CSV Cleaning & Transformation
- Feature Engineering Pipelines
- Data Exploration with AI Insights
- Lightweight alternative for local big data tasks

---

Architecture

- Chunk-based streaming processing
- Pandas-based core engine
- AI layer powered by scikit-learn
- CLI interface for automation

---

Current Status (v3.0)

✔ Core functionality implemented
✔ AI analytics integrated
✔ Multi-file support available

Work in Progress:

- Parallel processing optimization
- Memory-efficient streaming improvements
- Performance tuning

---

🛣️ Roadmap

v3.1

- True parallel execution (multi-core support)
- Faster chunk processing

v3.2

- Improved memory management
- Optimized AI pipeline

v4.0

- Distributed processing integration (Dask / Spark)
- Advanced caching system
- Real-time data pipeline support

---

Limitations

- Currently optimized for single-machine processing
- Not a distributed cluster system
- Performance depends on system RAM & CPU

---

Contributing

Contributions are welcome.

Areas where help is needed:

- Parallel processing implementation
- Performance optimization
- Testing on large datasets
- Documentation improvements

---

License

MIT License

---

Author

Arul Gnanakumar

---

Support

If you find this project useful, consider  it a ⭐ on GitHub.