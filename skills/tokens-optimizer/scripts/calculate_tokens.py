#!/usr/bin/env python3
"""
Calculates tokens usage from conversation text.
"""

import argparse
import sys
from datetime import datetime


def calculate_tokens(text):
    """
    Calculate tokens count from text.
    Estimation: 1 token ≈ 2.7 characters in Chinese.
    """
    char_count = len(text)
    token_count = int(char_count / 2.7)
    return token_count


def main():
    parser = argparse.ArgumentParser(
        description="Calculate tokens usage from conversation text."
    )
    parser.add_argument(
        "-f", "--file",
        help="Path to conversation file"
    )
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            conversation_text = f.read()
    else:
        conversation_text = sys.stdin.read()
    
    char_count = len(conversation_text)
    token_count = calculate_tokens(conversation_text)
    
    print(f"=== Tokens Usage Estimation ===")
    print(f"Characters: {char_count}")
    print(f"Tokens (estimated): {token_count}")
    print()
    
    print(f"Cost (estimated): ~¥{token_count * 0.02 / 1000:.4f}")
    print()
    
    print(f"Calculated at: {datetime.now()}")


if __name__ == "__main__":
    main()