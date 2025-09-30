# main.py
#!/usr/bin/env python3
"""
Main entry point for A/B Testing CDF Analyzer
"""

import argparse
from src.data.data_generator import ABTestDataGenerator
from src.analysis.cdf_calc import CDFAnalyzer
from src.visualizations.cdf_plots import CDFVisualizer

def main():
    parser = argparse.ArgumentParser(description='A/B Testing CDF Analyzer')
    parser.add_argument('--metric', type=str, default='session_duration', 
                       choices=['session_duration', 'conversion_time', 'page_load_time'],
                       help='Metric to analyze')
    parser.add_argument('--samples', type=int, default=1000,
                       help='Number of samples per variant')
    parser.add_argument('--output', type=str, default=None,
                       help='Output path for saving plots')
    
    args = parser.parse_args()
    
    # Generate sample data
    print("🚀 Generating sample A/B test data...")
    data_generator = ABTestDataGenerator()
    dataset = data_generator.create_sample_dataset()
    
    # Analyze the chosen metric
    print(f"📊 Analyzing {args.metric}...")
    analyzer = CDFAnalyzer()
    
    variant_a_data = dataset[args.metric]['A'][:args.samples]
    variant_b_data = dataset[args.metric]['B'][:args.samples]
    
    results = analyzer.compare_variants(variant_a_data, variant_b_data)
    
    # Display results
    print(f"\n📈 A/B Test Results for {args.metric}:")
    print(f"Sample sizes: A={results['variant_a']['size']}, B={results['variant_b']['size']}")
    print(f"KS Test p-value: {results['statistical_tests']['ks_test']['p_value']:.6f}")
    print(f"Mann-Whitney p-value: {results['statistical_tests']['mann_whitney']['p_value']:.6f}")
    print(f"Effect size (Cohen's d): {results['effect_size']:.3f}")
    
    # Create visualization
    print("\n🎨 Creating visualization...")
    CDFVisualizer.plot_matplotlib_cdf(results, args.metric, args.output)
    
    # Interactive plot
    fig = CDFVisualizer.create_interactive_plot(results, args.metric)
    fig.show()

if __name__ == "__main__":
    main()