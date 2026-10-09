#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified Field Theory Formula Visualization Generator

This script generates Nature-style visualizations for all important formulas in the unified field theory papers.
Supports visualization of vector potential equations, unified gravitational and electromagnetic field equations,
and cosmic grand unification equations.

Usage:
1. On Windows, to avoid encoding issues, first set console encoding to UTF-8:
   chcp 65001
2. Then run this script:
   python generate_all_visualizations.py
3. Or run specific visualizations:
   python generate_all_visualizations.py vector
   python generate_all_visualizations.py unified
   python generate_all_visualizations.py grand
"""

import os
import sys
import io
import subprocess
import time
from datetime import datetime

# Ensure UTF-8 encoding for standard output
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add environment variables for matplotlib to support Chinese fonts
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['MPLCONFIGDIR'] = os.path.join(os.path.dirname(__file__), '.matplotlib')

# Create matplotlib config directory if not exists
mpl_config_dir = os.environ['MPLCONFIGDIR']
os.makedirs(mpl_config_dir, exist_ok=True)

def create_directories():
    """Create necessary directory structure"""
    # Create visualization output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'visualizations')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        print(f"Output directory already exists: {output_dir}")
    
    # Create visualization scripts directory
    scripts_dir = os.path.join(os.path.dirname(__file__), 'visualization_scripts')
    if not os.path.exists(scripts_dir):
        print(f"Error: Visualization scripts directory does not exist: {scripts_dir}")
        return False
    
    return True

def check_requirements():
    """Check if required Python libraries are installed"""
    required_libraries = ['numpy', 'matplotlib']
    missing_libraries = []
    
    for lib in required_libraries:
        try:
            __import__(lib)
            print(f"✓ {lib} installed")
        except ImportError:
            missing_libraries.append(lib)
            print(f"✗ {lib} not installed")
    
    if missing_libraries:
        print("\nPlease install missing libraries first:")
        print(f"pip install {' '.join(missing_libraries)}")
        return False
    
    return True

def run_visualization_script(script_path, description):
    """Run a single visualization script"""
    print(f"\nGenerating {description}...")
    start_time = time.time()
    
    try:
        # Set environment to ensure proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run([sys.executable, script_path], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True, 
                              encoding='utf-8',
                              timeout=300,  # 5 minutes timeout
                              env=env)
        
        if result.returncode == 0:
            elapsed_time = time.time() - start_time
            print(f"✓ {description} generated successfully (time: {elapsed_time:.2f} seconds)")
            # Print last lines of script output
            output_lines = result.stdout.strip().split('\n')
            if output_lines:
                print("  Output:", output_lines[-1])
            return True
        else:
            print(f"✗ {description} generation failed")
            print("Error message:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Exception occurred while generating {description}: {str(e)}")
        return False

def generate_all_visualizations():
    """Generate all visualization images"""
    print("="*80)
    print("Unified Field Theory Formula Visualization System")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Create necessary directories
    if not create_directories():
        return False
    
    # Check dependencies
    print("\nChecking Python library dependencies...")
    if not check_requirements():
        return False
    
    # Define visualization scripts to run
    base_dir = os.path.dirname(__file__)
    scripts = [
        {
            'path': os.path.join(base_dir, 'visualization_scripts', 'vector_potential_visualization.py'),
            'description': 'Vector Potential Equation Visualization'
        },
        {
            'path': os.path.join(base_dir, 'visualization_scripts', 'unified_field_equation_visualization.py'),
            'description': 'Unified Gravitational and Electromagnetic Field Equation Visualization'
        },
        {
            'path': os.path.join(base_dir, 'visualization_scripts', 'grand_unification_visualization.py'),
            'description': 'Cosmic Grand Unification Equation Visualization'
        }
    ]
    
    # Run all scripts
    print("\nStarting visualization generation...")
    success_count = 0
    total_count = len(scripts)
    
    for script in scripts:
        if run_visualization_script(script['path'], script['description']):
            success_count += 1
    
    # Generate summary report
    print("\n" + "="*80)
    print(f"Visualization generation summary: {success_count}/{total_count} succeeded")
    output_dir = os.path.join(base_dir, 'visualizations')
    print(f"Output directory: {output_dir}")
    
    if success_count == total_count:
        print("✓ All visualizations generated successfully!")
    else:
        print("✗ Some visualizations failed to generate, please check error messages.")
    
    print("="*80)
    return success_count == total_count

def generate_specific_visualization(script_name):
    """Generate specific visualization image"""
    base_dir = os.path.dirname(__file__)
    script_map = {
        'vector': os.path.join(base_dir, 'visualization_scripts', 'vector_potential_visualization.py'),
        'unified': os.path.join(base_dir, 'visualization_scripts', 'unified_field_equation_visualization.py'),
        'grand': os.path.join(base_dir, 'visualization_scripts', 'grand_unification_visualization.py')
    }
    
    description_map = {
        'vector': 'Vector Potential Equation Visualization',
        'unified': 'Unified Gravitational and Electromagnetic Field Equation Visualization',
        'grand': 'Cosmic Grand Unification Equation Visualization'
    }
    
    if script_name not in script_map:
        print(f"Error: Unknown visualization type '{script_name}'")
        print("Available visualization types: vector, unified, grand")
        return False
    
    create_directories()
    check_requirements()
    
    return run_visualization_script(script_map[script_name], description_map[script_name])

if __name__ == "__main__":
    # 处理命令行参数
    if len(sys.argv) > 1:
        # 生成特定的可视化
        generate_specific_visualization(sys.argv[1])
    else:
        # 生成所有可视化
        generate_all_visualizations()