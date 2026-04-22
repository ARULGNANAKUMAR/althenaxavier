#!/usr/bin/env python3
"""
AlthenaXavier CLI - Big Data Processing with AI
Usage: althenaxavier [COMMAND] [OPTIONS]
"""

import argparse
import sys
from pathlib import Path
from engine import AlthenaXavierEngine

def main():
    parser = argparse.ArgumentParser(
        description="AlthenaXavier v3.0 - AI-Powered Big Data Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file processing
  althenaxavier process data.csv --op sum --column sales
  
  # Multiple files
  althenaxavier process "data/*.csv" --op mean --column price
  
  # AI Analysis
  althenaxavier ai data.csv --column revenue --analyze all
  
  # Compare multiple files
  althenaxavier compare file1.csv file2.csv --column profit
  
  # Forecast
  althenaxavier forecast sales.csv --column revenue --periods 30
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # PROCESS command
    process_parser = subparsers.add_parser('process', help='Process data')
    process_parser.add_argument('files', help='File or pattern (e.g., "data/*.csv")')
    process_parser.add_argument('--op', required=True, 
                               choices=['sum', 'mean', 'min', 'max', 'count', 'describe'])
    process_parser.add_argument('--column', required=True)
    process_parser.add_argument('--type', default='csv', 
                               choices=['csv', 'parquet', 'json', 'excel'])
    process_parser.add_argument('--parallel', action='store_true', help='Enable parallel processing')
    
    # AI command
    ai_parser = subparsers.add_parser('ai', help='AI-powered analysis')
    ai_parser.add_argument('file', help='CSV file path')
    ai_parser.add_argument('--column', required=True)
    ai_parser.add_argument('--analyze', default='all',
                          choices=['anomaly', 'forecast', 'cluster', 'trend', 'all'])
    ai_parser.add_argument('--periods', type=int, default=10, help='Forecast periods')
    
    # COMPARE command
    compare_parser = subparsers.add_parser('compare', help='Compare multiple files')
    compare_parser.add_argument('files', nargs='+', help='Files to compare')
    compare_parser.add_argument('--column', required=True)
    compare_parser.add_argument('--op', default='mean', 
                               choices=['sum', 'mean', 'min', 'max'])
    
    # FORECAST command
    forecast_parser = subparsers.add_parser('forecast', help='Predict future values')
    forecast_parser.add_argument('file', help='CSV file path')
    forecast_parser.add_argument('--column', required=True)
    forecast_parser.add_argument('--periods', type=int, default=10)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    engine = AlthenaXavierEngine(parallel_workers=None if not getattr(args, 'parallel', False) else None)
    
    try:
        if args.command == 'process':
            result = engine.process_files(
                _get_file_list(args.files),
                args.op,
                args.column,
                file_type=args.type
            )
            print(f"\n✅ Result: {result}")
            
        elif args.command == 'ai':
            result = engine.ai_analyze(args.file, args.column, args.analyze)
            _print_ai_results(result)
            
        elif args.command == 'compare':
            result = engine.process_files(args.files, args.op, args.column)
            print(f"\n📊 Comparison Result ({args.op} of '{args.column}'):")
            for item in result:
                print(f"  {Path(item['file']).name}: {item['result']}")
                
        elif args.command == 'forecast':
            result = engine.ai_analyze(args.file, args.column, 'forecast')
            if 'forecast' in result:
                print(f"\n🔮 Forecast for '{args.column}':")
                print(f"  Trend: {result['forecast']['trend']}")
                print(f"  Confidence: {result['forecast']['confidence']}%")
                print(f"  Next {args.periods} values: {result['forecast']['next_values'][:args.periods]}")
        
        print("\n✓ Operation completed successfully")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def _get_file_list(pattern):
    """Convert file pattern to list of files"""
    from glob import glob
    
    if '*' in pattern:
        return glob(pattern)
    return [pattern]


def _print_ai_results(results):
    """Pretty print AI analysis results"""
    print("\n🤖 AI Analysis Results:")
    print("=" * 50)
    
    if 'statistics' in results:
        print("\n📊 Statistics:")
        stats = results['statistics']
        print(f"  Count: {stats['count']:,}")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Std Dev: {stats['std']:.2f}")
        print(f"  Min: {stats['min']:.2f}")
        print(f"  Max: {stats['max']:.2f}")
    
    if 'anomalies' in results:
        print("\n⚠️ Anomalies Detected:")
        print(f"  Count: {results['anomalies']['count']}")
        print(f"  Percentage: {results['anomalies']['percentage']:.2f}%")
        if results['anomalies']['values']:
            print(f"  Sample: {results['anomalies']['values'][:5]}")
    
    if 'forecast' in results:
        print("\n🔮 Forecast:")
        print(f"  Trend: {results['forecast']['trend']}")
        print(f"  Confidence: {results['forecast']['confidence']}%")
        print(f"  Next values: {results['forecast']['next_values'][:5]}")
    
    if 'trend' in results:
        print("\n📈 Trend Analysis:")
        print(f"  Direction: {results['trend']['trend']}")
        print(f"  Change: {results['trend']['change_percentage']}%")
    
    if 'clusters' in results:
        print("\n🎯 Pattern Clusters:")
        print(f"  Clusters found: {results['clusters']['n_clusters']}")


if __name__ == "__main__":
    main()