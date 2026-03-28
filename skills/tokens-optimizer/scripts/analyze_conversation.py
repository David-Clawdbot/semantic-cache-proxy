#!/usr/bin/env python3
"""
Analyzes conversation history and provides tokens optimization recommendations.
"""

import argparse
import sys
from datetime import datetime


def analyze_conversation(conversation_text):
    """
    Analyze conversation text and provide optimization recommendations.
    """
    lines = conversation_text.strip().split('\n')
    
    recommendations = []
    issues = []
    
    # Check for repetition
    seen_lines = set()
    for i, line in enumerate(lines):
        stripped_line = line.strip().lower()
        if stripped_line and stripped_line in seen_lines:
            issues.append(f"Line {i+1}: Repeated content detected")
        seen_lines.add(stripped_line)
    
    # Check for long sentences
    for i, line in enumerate(lines):
        word_count = len(line.split())
        if word_count > 30:
            issues.append(f"Line {i+1}: Sentence is too long ({word_count} words)")
    
    # Generate recommendations
    if issues:
        recommendations.append("Issues found:")
        for issue in issues:
            recommendations.append(f"  - {issue}")
        
        recommendations.append("\nRecommendations:")
        recommendations.append("  1. Remove repeated content")
        recommendations.append("  2. Split long sentences into shorter ones")
        recommendations.append("  3. Be more specific about your requirements")
        recommendations.append("  4. Avoid unnecessary background information")
    else:
        recommendations.append("Conversation is already well-optimized!")
        recommendations.append("\nTips for continued efficiency:")
        recommendations.append("  1. Keep questions clear and focused")
        recommendations.append("  2. Provide only relevant context")
        recommendations.append("  3. Break complex tasks into smaller steps")
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(
        description="Analyze conversation history and provide tokens optimization recommendations."
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to conversation file to analyze"
    )
    
    args = parser.parse_args()
    
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                conversation_text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
    else:
        conversation_text = sys.stdin.read()
    
    recommendations = analyze_conversation(conversation_text)
    
    print("\n=== Tokens Optimization Analysis ===\n")
    for rec in recommendations:
        print(rec)
    print()
    
    print(f"Analysis completed: {datetime.now()}")


if __name__ == "__main__":
    main()