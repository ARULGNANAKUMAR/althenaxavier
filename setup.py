from setuptools import setup
from pathlib import Path

setup(
    name="althenaxavier",
    version="3.0.0",
    author="Arul Gnanakumar",
    description="AI-Powered Big Data Processing Engine - PySpark Alternative",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    
    py_modules=['engine', 'cli'],
    
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.21.0',
        'psutil>=5.9.0',
        'tqdm>=4.64.0',
        'scikit-learn>=1.2.0',  # For AI features
        'scipy>=1.9.0',
    ],
    
    extras_require={
        'full': [
            'pyarrow>=10.0.0',      # Parquet support
            'openpyxl>=3.0.0',      # Excel support
            'fastparquet>=2023.0.0',
        ],
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
        ]
    },
    
    entry_points={
        'console_scripts': [
            'althenaxavier=cli:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    
    python_requires='>=3.8',
)