#!/usr/bin/env python3
"""
Tracks tokens usage and provides statistics.
"""

import argparse
import json
import os
from datetime import datetime, timedelta


def load_usage_data(data_file):
    """
    Load usage data from file.
    """
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"sessions": []}


def save_usage_data(data_file, data):
    """
    Save usage data to file.
    """
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)


def track_usage(data_file, tokens_used, session_id=None):
    """
    Track tokens usage.
    """
    data = load_usage_data(data_file)
    
    session = {
        "id": session_id or str(len(data["sessions"]) + 1),
        "timestamp": datetime.now().isoformat(),
        "tokens_used": tokens_used
    }
    
    data["sessions"].append(session)
    save_usage_data(data_file, data)
    
    return data


def get_statistics(data_file, days=7):
    """
    Get usage statistics for the last N days.
    """
    data = load_usage_data(data_file)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    recent_sessions = []
    for session in data["sessions"]:
        session_date = datetime.fromisoformat(session["timestamp"])
        if start_date <= session_date <= end_date:
            recent_sessions.append(session)
    
    if not recent_sessions:
        return {
            "period": f"Last {days} days",
            "total_sessions": 0,
            "total_tokens": 0,
            "avg_tokens_per_session": 0,
            "peak_tokens": 0
        }
    
    total_tokens = sum(session["tokens_used"] for session in recent_sessions)
    avg_tokens = total_tokens / len(recent_sessions)
    peak_tokens = max(session["tokens_used"] for session in recent_sessions)
    
    return {
        "period": f"Last {days} days",
        "total_sessions": len(recent_sessions),
        "total_tokens": total_tokens,
        "avg_tokens_per_session": round(avg_tokens, 2),
        "peak_tokens": peak_tokens
    }


def main():
    parser = argparse.ArgumentParser(
        description="Track tokens usage and provide statistics."
    )
    parser.add_argument(
        "-d", "--data-file",
        default="tokens_usage.json",
        help="Path to data file (default: tokens_usage.json)"
    )
    parser.add_argument(
        "-t", "--track",
        type=int,
        help="Track new tokens usage"
    )
    parser.add_argument(
        "-s", "--statistics",
        type=int,
        default=7,
        help="Get statistics for last N days (default: 7)"
    )
    
    args = parser.parse_args()
    
    if args.track is not None:
        data = track_usage(args.data_file, args.track)
        print(f"Tracked {args.track} tokens used")
    else:
        stats = get_statistics(args.data_file, args.statistics)
        print("\n=== Tokens Usage Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    main()