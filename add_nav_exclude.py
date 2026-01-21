import os
import re
from pathlib import Path

def parse_frontmatter(content):
    """Parse front matter from markdown content."""
    if not content.startswith('---'):
        return None, None, content
    
    # Find the closing ---
    end_idx = content.find('\n---', 3)
    if end_idx == -1:
        return None, None, content
    
    frontmatter_text = content[3:end_idx].strip()
    rest_content = content[end_idx + 5:].lstrip('\n')
    
    return frontmatter_text, rest_content

def has_parent_or_grandparent(frontmatter_text):
    """Check if front matter has parent or grand_parent."""
    if not frontmatter_text:
        return False
    
    # Check for parent: or grand_parent: (case sensitive, with optional quotes)
    parent_pattern = r'^parent\s*:'
    grandparent_pattern = r'^grand_parent\s*:'
    
    for line in frontmatter_text.split('\n'):
        line_stripped = line.strip()
        if re.match(parent_pattern, line_stripped, re.IGNORECASE) or \
           re.match(grandparent_pattern, line_stripped, re.IGNORECASE):
            return True
    return False

def has_nav_exclude(frontmatter_text):
    """Check if front matter already has nav_exclude."""
    if not frontmatter_text:
        return False
    
    nav_exclude_pattern = r'^nav_exclude\s*:'
    for line in frontmatter_text.split('\n'):
        line_stripped = line.strip()
        if re.match(nav_exclude_pattern, line_stripped, re.IGNORECASE):
            return True
    return False

def add_nav_exclude_to_frontmatter(frontmatter_text):
    """Add nav_exclude: true to front matter."""
    if not frontmatter_text:
        return "nav_exclude: true"
    
    # Add nav_exclude: true at the end of front matter
    return frontmatter_text + "\nnav_exclude: true"

def process_markdown_file(file_path):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading {file_path}: {e}"
    
    # Check if file has front matter
    if not content.startswith('---'):
        return "no_frontmatter"
    
    # Parse front matter
    frontmatter_text, rest_content = parse_frontmatter(content)
    
    if frontmatter_text is None:
        return "no_frontmatter"
    
    # Check if it already has nav_exclude
    if has_nav_exclude(frontmatter_text):
        return "has_nav_exclude"
    
    # Check if it has parent or grand_parent
    if has_parent_or_grandparent(frontmatter_text):
        return "has_parent_or_grandparent"
    
    # Add nav_exclude: true to front matter
    new_frontmatter = add_nav_exclude_to_frontmatter(frontmatter_text)
    new_content = "---\n" + new_frontmatter + "\n---\n\n" + rest_content
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return "success"
    except Exception as e:
        return f"Error writing {file_path}: {e}"

def main():
    # Determine the source folder
    base_dir = Path(__file__).parent
    src_folder = base_dir / "src"
    
    if not src_folder.exists():
        print(f"Error: 'src' folder not found!")
        return
    
    print(f"Processing files in: {src_folder}")
    
    # Find all .md files recursively
    md_files = list(src_folder.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")
    
    processed_count = 0
    skipped_no_frontmatter = 0
    skipped_has_nav_exclude = 0
    skipped_has_parent = 0
    error_count = 0
    
    for md_file in md_files:
        result = process_markdown_file(md_file)
        relative_path = md_file.relative_to(base_dir)
        
        if result == "success":
            processed_count += 1
            print(f"[OK] Added nav_exclude: {relative_path}")
        elif result == "no_frontmatter":
            skipped_no_frontmatter += 1
        elif result == "has_nav_exclude":
            skipped_has_nav_exclude += 1
        elif result == "has_parent_or_grandparent":
            skipped_has_parent += 1
        else:
            error_count += 1
            print(f"[ERROR] {relative_path}: {result}")
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Files processed (nav_exclude added): {processed_count}")
    print(f"  Skipped (no front matter): {skipped_no_frontmatter}")
    print(f"  Skipped (already has nav_exclude): {skipped_has_nav_exclude}")
    print(f"  Skipped (has parent/grand_parent): {skipped_has_parent}")
    print(f"  Errors: {error_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()

