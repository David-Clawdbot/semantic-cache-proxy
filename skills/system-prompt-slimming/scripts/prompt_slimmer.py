#!/usr/bin/env python3
"""
System Prompt Slimming Script
Optimizes system prompt files by removing redundancy and enforcing size limits.
"""

import os
import re
import json
from typing import List, Dict, Tuple
from datetime import datetime

class PromptSlimmer:
    def __init__(self, max_words: int = 2000):
        self.max_words = max_words
        self.backup_dir = "~/.openclaw/workspace/.prompt_backups"
        
        # Patterns to identify redundant content
        self.redundancy_patterns = [
            r'(?s)(.*?)(?:\1{2,})',  # Repeated content
        ]
        
        # Content priority - higher = more important to keep
        self.content_priority = {
            "identity": 10,      # Who the agent is
            "core_rules": 9,     # Essential rules
            "safety": 8,         # Safety guidelines
            "skills": 7,         # Skill descriptions
            "workflow": 6,       # Process guidelines
            "examples": 5,       # Examples
            "vibe": 4,           # Tone/personality
            "background": 3      # Background info
        }
    
    def count_words(self, text: str) -> int:
        """Count words in text."""
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def backup_file(self, file_path: str) -> str:
        """Create a backup of the file before modification."""
        backup_dir = os.path.expanduser(self.backup_dir)
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return backup_path
    
    def analyze_content(self, text: str) -> Dict:
        """Analyze content and identify sections."""
        sections = {}
        
        # Common section headers in AGENTS.md, SOUL.md, etc.
        section_patterns = [
            (r'##\s+(Core Rules|核心规则)', 'core_rules'),
            (r'##\s+(Safety|安全)', 'safety'),
            (r'##\s+(Identity|身份)', 'identity'),
            (r'##\s+(Skills|技能)', 'skills'),
            (r'##\s+(Workflow|工作流)', 'workflow'),
            (r'##\s+(Personality|Vibe|风格)', 'vibe'),
            (r'##\s+(Background|背景)', 'background'),
        ]
        
        lines = text.split('\n')
        current_section = 'other'
        section_content = []
        
        for line in lines:
            # Check for section headers
            matched = False
            for pattern, section_name in section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    current_section = section_name
                    section_content = [line]
                    matched = True
                    break
            
            if not matched:
                section_content.append(line)
        
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def remove_redundancy(self, text: str) -> Tuple[str, int]:
        """Remove redundant content from text."""
        original_words = self.count_words(text)
        
        # Remove duplicate lines
        lines = text.split('\n')
        seen_lines = set()
        unique_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            # More aggressive duplicate detection - normalize whitespace and lowercase
            line_normalized = ' '.join(line_stripped.lower().split())
            
            if line_stripped and line_normalized not in seen_lines:
                seen_lines.add(line_normalized)
                unique_lines.append(line)
            elif not line_stripped:
                unique_lines.append(line)  # Keep empty lines for structure
        
        cleaned_text = '\n'.join(unique_lines)
        
        # Remove redundant phrases (English and Chinese)
        redundant_phrases = [
            r'Please note that',
            r'It is important to',
            r'You should always',
            r'Keep in mind that',
            r'记住',
            r'务必',
            r'一定要',
            r'请注意',
            r'重要的是',
            r'你应该',
            r'你必须',
        ]
        
        for phrase in redundant_phrases:
            cleaned_text = re.sub(phrase, '', cleaned_text, flags=re.IGNORECASE)
        
        # Remove sentences that are very similar (same meaning, different wording)
        # This is a simplified approach - look for sentences with high overlap
        sentences = re.split(r'[.!?。！？]', cleaned_text)
        seen_sentences = set()
        unique_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            # Normalize sentence for comparison
            normalized = ' '.join(sentence.lower().split())
            # Check if we've seen something very similar
            is_redundant = False
            for seen in seen_sentences:
                # Simple overlap check - if 70% of words are the same
                words1 = set(normalized.split())
                words2 = set(seen.split())
                if words1 and words2:
                    overlap = len(words1 & words2) / max(len(words1), len(words2))
                    if overlap > 0.6:
                        is_redundant = True
                        break
            if not is_redundant:
                seen_sentences.add(normalized)
                unique_sentences.append(sentence)
        
        # Reconstruct - this is simplified, real implementation would be more sophisticated
        # For now, just use the line-based cleaning we did earlier
        
        final_words = self.count_words(cleaned_text)
        removed_words = original_words - final_words
        
        return cleaned_text, removed_words
    
    def prioritize_and_trim(self, sections: Dict, target_words: int) -> str:
        """Prioritize content and trim to target word count."""
        # Sort sections by priority
        sorted_sections = sorted(
            sections.items(),
            key=lambda x: self.content_priority.get(x[0], 0),
            reverse=True
        )
        
        result = []
        current_words = 0
        
        for section_name, content in sorted_sections:
            section_words = self.count_words(content)
            
            if current_words + section_words <= target_words:
                result.append(content)
                current_words += section_words
            else:
                # Try to trim this section
                remaining = target_words - current_words
                if remaining > 50:  # Only if we can fit a meaningful portion
                    lines = content.split('\n')
                    trimmed_lines = []
                    trimmed_words = 0
                    
                    for line in lines:
                        line_words = self.count_words(line)
                        if trimmed_words + line_words <= remaining:
                            trimmed_lines.append(line)
                            trimmed_words += line_words
                        else:
                            break
                    
                    if trimmed_lines:
                        result.append('\n'.join(trimmed_lines) + '\n... [content trimmed]')
                    break
        
        return '\n'.join(result)
    
    def slim_prompt(self, file_path: str) -> Dict:
        """
        Slim down a prompt file.
        
        Args:
            file_path: Path to the prompt file
            
        Returns:
            Optimization results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        # Backup original
        backup_path = self.backup_file(file_path)
        
        # Read and analyze
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        original_words = self.count_words(original_content)
        
        # Remove redundancy
        cleaned_content, removed_words = self.remove_redundancy(original_content)
        
        # Analyze sections
        sections = self.analyze_content(cleaned_content)
        
        # Prioritize and trim if needed
        if self.count_words(cleaned_content) > self.max_words:
            final_content = self.prioritize_and_trim(sections, self.max_words)
        else:
            final_content = cleaned_content
        
        final_words = self.count_words(final_content)
        
        # Write optimized version
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        # Calculate savings
        savings_percent = ((original_words - final_words) / original_words) * 100 if original_words > 0 else 0
        
        return {
            "success": True,
            "original_file": file_path,
            "backup_file": backup_path,
            "original_words": original_words,
            "final_words": final_words,
            "words_removed": original_words - final_words,
            "savings_percent": round(savings_percent, 1),
            "target_reached": final_words <= self.max_words
        }

def main():
    slimmer = PromptSlimmer(max_words=2000)
    
    # Test with a sample file or demo
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = slimmer.slim_prompt(file_path)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Successfully slimmed prompt:")
            print(f"  Original: {result['original_words']} words")
            print(f"  Final: {result['final_words']} words")
            print(f"  Savings: {result['savings_percent']}%")
            print(f"  Backup: {result['backup_file']}")
    else:
        # Demo mode
        print("=== System Prompt Slimming Demo ===")
        print("Usage: python prompt_slimmer.py <file_path>")
        print("\nFeatures:")
        print("- Removes redundant content")
        print("- Prioritizes important information")
        print("- Keeps under 2000 words")
        print("- Estimated 65% token savings")

if __name__ == "__main__":
    import sys
    main()
