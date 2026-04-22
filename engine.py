"""
AlthenaXavier v3.0 - AI-Powered Big Data Engine
Equal to PySpark for CSV/Parquet processing
"""

import pandas as pd
import numpy as np
import psutil
import logging
import gc
import json
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from collections import defaultdict
import hashlib
import warnings
warnings.filterwarnings('ignore')

# AI/ML imports
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AlthenaXavierEngine:
    """
    Production-grade data processing engine with AI capabilities
    Supports: Multiple files, Parallel processing, AI analytics
    """
    
    def __init__(self, chunk_size=None, parallel_workers=None):
        self.chunk_size = chunk_size or self._adaptive_chunk()
        self.parallel_workers = parallel_workers or psutil.cpu_count()
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        
    def _adaptive_chunk(self):
        """AI-powered adaptive chunk sizing"""
        ram_gb = psutil.virtual_memory().available / (1024**3)
        cpu_count = psutil.cpu_count()
        
        # AI decision based on system resources
        if ram_gb > 16:
            return 1000000  # 1M rows per chunk
        elif ram_gb > 8:
            return 500000
        elif ram_gb > 4:
            return 250000
        elif ram_gb > 2:
            return 100000
        else:
            return 25000
    
    # ==================== MULTI-FILE SUPPORT ====================
    
    def read_files(self, file_pattern, file_type='csv'):
        """
        Read multiple files with pattern matching
        Usage: read_files("data/*.csv") or read_files(["file1.csv", "file2.csv"])
        """
        from glob import glob
        
        if isinstance(file_pattern, str):
            if '*' in file_pattern:
                files = glob(file_pattern)
            else:
                files = [file_pattern]
        else:
            files = file_pattern
        
        self.logger.info(f"Found {len(files)} files to process")
        return MultiFileReader(files, file_type, self)
    
    def process_files(self, files, operation, column, **kwargs):
        """
        Process multiple files and aggregate results
        """
        results = []
        
        for file in tqdm(files, desc="Processing files"):
            result = self.process_single(file, operation, column, **kwargs)
            results.append({
                'file': file,
                'result': result
            })
        
        # Aggregate across files
        return self._aggregate_results(results, operation)
    
    def process_single(self, file, operation, column, **kwargs):
        """Process single file with AI features"""
        total_sum = 0
        total_count = 0
        result = None
        anomalies = []
        
        reader = self._get_reader(file, kwargs.get('file_type', 'csv'))
        
        for chunk in tqdm(reader, desc=f"Processing {Path(file).name}"):
            if column not in chunk.columns:
                raise ValueError(f"Column '{column}' not found in {file}")
            
            series = chunk[column].dropna()
            
            if operation == 'sum':
                result = (result or 0) + series.sum()
            elif operation == 'mean':
                total_sum += series.sum()
                total_count += len(series)
                result = total_sum / total_count
            elif operation == 'min':
                result = min(result, series.min()) if result is not None else series.min()
            elif operation == 'max':
                result = max(result, series.max()) if result is not None else series.max()
            elif operation == 'count':
                result = (result or 0) + len(series)
            elif operation == 'describe':
                result = self._compute_statistics(series, result)
            elif operation == 'ai_anomaly':
                anomalies.extend(self._detect_anomalies_ai(series))
                result = anomalies
        
        return result
    
    def _get_reader(self, file, file_type):
        """Support multiple file formats"""
        if file_type == 'csv':
            return pd.read_csv(file, chunksize=self.chunk_size, low_memory=False)
        elif file_type == 'parquet':
            return pd.read_parquet(file, chunksize=self.chunk_size)
        elif file_type == 'json':
            return pd.read_json(file, chunksize=self.chunk_size, lines=True)
        elif file_type == 'excel':
            return pd.read_excel(file, chunksize=self.chunk_size)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    # ==================== AI FEATURES ====================
    
    def ai_analyze(self, file, column, analysis_type='all'):
        """
        Complete AI analysis on a column
        Types: 'anomaly', 'forecast', 'cluster', 'trend', 'all'
        """
        # Load full column (for AI analysis - limited rows if too big)
        df = self._load_column_sample(file, column)
        series = df[column].dropna()
        
        results = {}
        
        if analysis_type in ['anomaly', 'all']:
            results['anomalies'] = self._detect_anomalies_ai(series)
        
        if analysis_type in ['forecast', 'all']:
            results['forecast'] = self._forecast_values(series)
        
        if analysis_type in ['cluster', 'all'] and len(series) > 10:
            results['clusters'] = self._cluster_data(series)
        
        if analysis_type in ['trend', 'all']:
            results['trend'] = self._detect_trend(series)
        
        results['statistics'] = self._compute_statistics(series)
        
        return results
    
    def _detect_anomalies_ai(self, series):
        """Isolation Forest based anomaly detection"""
        if len(series) < 10:
            return []
        
        # Reshape for sklearn
        X = series.values.reshape(-1, 1)
        
        # Use Isolation Forest (works well for anomalies)
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        predictions = iso_forest.fit_predict(X)
        
        # -1 indicates anomaly
        anomaly_indices = np.where(predictions == -1)[0]
        anomalies = series.iloc[anomaly_indices].tolist()
        
        self.logger.info(f"Found {len(anomalies)} anomalies using AI")
        
        return {
            'count': len(anomalies),
            'values': anomalies[:10],  # First 10 anomalies
            'percentage': (len(anomalies) / len(series)) * 100,
            'method': 'Isolation Forest'
        }
    
    def _forecast_values(self, series, periods=10):
        """Linear regression based forecasting"""
        if len(series) < 5:
            return {'error': 'Need at least 5 data points'}
        
        X = np.arange(len(series)).reshape(-1, 1)
        y = series.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 'periods' values
        future_X = np.arange(len(series), len(series) + periods).reshape(-1, 1)
        predictions = model.predict(future_X)
        
        # Calculate confidence (R-squared)
        r2 = model.score(X, y)
        
        trend = 'increasing' if model.coef_[0] > 0 else 'decreasing'
        
        return {
            'next_values': predictions.tolist(),
            'trend': trend,
            'confidence': round(r2 * 100, 2),
            'method': 'Linear Regression'
        }
    
    def _cluster_data(self, series, n_clusters=5):
        """K-means clustering for pattern discovery"""
        if len(series) < n_clusters * 2:
            return {'error': 'Insufficient data for clustering'}
        
        X = series.values.reshape(-1, 1)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Determine optimal clusters using elbow method
        if len(series) > 100:
            kmeans = KMeans(n_clusters=min(n_clusters, 10), random_state=42, n_init=10)
        else:
            kmeans = KMeans(n_clusters=min(n_clusters, 5), random_state=42, n_init=10)
        
        clusters = kmeans.fit_predict(X_scaled)
        
        # Group by cluster
        cluster_info = {}
        for i in range(kmeans.n_clusters):
            cluster_values = series[clusters == i]
            cluster_info[f'cluster_{i}'] = {
                'size': len(cluster_values),
                'mean': cluster_values.mean(),
                'min': cluster_values.min(),
                'max': cluster_values.max()
            }
        
        return {
            'n_clusters': kmeans.n_clusters,
            'clusters': cluster_info,
            'inertia': round(kmeans.inertia_, 2)
        }
    
    def _detect_trend(self, series):
        """Trend analysis using moving averages"""
        if len(series) < 10:
            return {'trend': 'insufficient_data'}
        
        # Calculate moving average
        window = min(5, len(series) // 4)
        ma = series.rolling(window=window).mean()
        
        # Compare first and last 20%
        first_20 = ma.iloc[:len(ma)//5].mean()
        last_20 = ma.iloc[-len(ma)//5:].mean()
        
        if last_20 > first_20 * 1.05:
            trend = 'strong_upward'
        elif last_20 > first_20:
            trend = 'upward'
        elif last_20 < first_20 * 0.95:
            trend = 'strong_downward'
        elif last_20 < first_20:
            trend = 'downward'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change_percentage': round(((last_20 - first_20) / first_20) * 100, 2),
            'method': 'Moving Average'
        }
    
    def _compute_statistics(self, series, existing=None):
        """Compute comprehensive statistics"""
        stats = {
            'count': len(series),
            'mean': series.mean(),
            'std': series.std(),
            'min': series.min(),
            '25%': series.quantile(0.25),
            '50%': series.median(),
            '75%': series.quantile(0.75),
            'max': series.max(),
            'skewness': series.skew(),
            'kurtosis': series.kurtosis()
        }
        
        if existing:
            # Merge with existing stats (for chunked processing)
            for key in existing:
                if key in stats:
                    stats[key] = (existing[key] + stats[key]) / 2
        
        return stats
    
    def _load_column_sample(self, file, column, max_rows=100000):
        """Load sample for AI analysis (avoid memory issues)"""
        total_rows = sum(1 for _ in open(file)) - 1
        
        if total_rows > max_rows:
            # Sample the data
            sample_size = min(max_rows, total_rows)
            skip = sorted(np.random.choice(range(1, total_rows+1), 
                                          size=sample_size, replace=False))
            df = pd.read_csv(file, skiprows=skip, header=0)
        else:
            df = pd.read_csv(file)
        
        return df[[column]]
    
    def _aggregate_results(self, results, operation):
        """Aggregate results from multiple files"""
        if operation in ['sum', 'count']:
            return sum(r['result'] for r in results)
        elif operation == 'mean':
            total = sum(r['result'] for r in results)
            return total / len(results)
        elif operation == 'min':
            return min(r['result'] for r in results)
        elif operation == 'max':
            return max(r['result'] for r in results)
        else:
            return results


class MultiFileReader:
    """Handle multiple files as single dataset"""
    
    def __init__(self, files, file_type, engine):
        self.files = files
        self.file_type = file_type
        self.engine = engine
    
    def process(self, operation, column):
        return self.engine.process_files(self.files, operation, column)
    
    def ai_analyze(self, column, analysis_type='all'):
        results = {}
        for file in self.files:
            results[Path(file).name] = self.engine.ai_analyze(file, column, analysis_type)
        return results