import os
import re
from pathlib import Path

def parse_frontmatter(content):
    """Parse front matter from markdown content, preserving original format."""
    if not content.startswith('---'):
        return None, None, content
    
    # Find the closing ---
    end_idx = content.find('\n---', 3)
    if end_idx == -1:
        return None, None, content
    
    frontmatter_text = content[3:end_idx].strip()
    rest_content = content[end_idx + 5:].lstrip('\n')
    
    # Extract title from front matter without modifying the original format
    title = None
    for line in frontmatter_text.split('\n'):
        if line.strip().startswith('title:'):
            # Extract title value, handling quotes
            title_part = line.split(':', 1)[1].strip()
            title = title_part.strip('"\'')
            break
    
    return frontmatter_text, title, rest_content

def has_h1_heading(content):
    """Check if content starts with an h1 heading."""
    # Remove leading whitespace and check for # heading
    lines = content.strip().split('\n')
    if lines and lines[0].strip().startswith('# '):
        # Make sure it's h1, not h2 or higher
        if lines[0].strip().startswith('# ') and not lines[0].strip().startswith('##'):
            return True
    return False

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
    frontmatter_text, title, rest_content = parse_frontmatter(content)
    
    if frontmatter_text is None:
        return "no_frontmatter"
    
    # Check if title exists
    if title is None:
        return "no_title"
    
    # Check if h1 already exists right after front matter
    if has_h1_heading(rest_content):
        return "has_h1"
    
    # Reconstruct the file with h1 heading, preserving original front matter format
    new_content = "---\n" + frontmatter_text + "\n---\n\n"
    new_content += f"# {title}\n\n"
    new_content += rest_content
    
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
    print(f"Found {len(md_files)} markdown files")
    
    skipped_files = []
    processed_count = 0
    error_count = 0
    
    for md_file in md_files:
        result = process_markdown_file(md_file)
        relative_path = md_file.relative_to(base_dir)
        
        if result == "success":
            processed_count += 1
            print(f"[OK] Processed: {relative_path}")
        elif result in ["no_frontmatter", "no_title", "has_h1"]:
            skipped_files.append((relative_path, result))
            print(f"[SKIP] Skipped ({result}): {relative_path}")
        else:
            error_count += 1
            skipped_files.append((relative_path, result))
            print(f"[ERROR] Error: {relative_path} - {result}")
    
    # Write skipped files to txt file
    skipped_file_path = base_dir / "skipped_files.txt"
    with open(skipped_file_path, 'w', encoding='utf-8') as f:
        f.write("Skipped Files Report\n")
        f.write("=" * 50 + "\n\n")
        for file_path, reason in skipped_files:
            f.write(f"{file_path} - {reason}\n")
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Processed: {processed_count}")
    print(f"  Skipped: {len(skipped_files)}")
    print(f"  Errors: {error_count}")
    print(f"\nSkipped files list saved to: {skipped_file_path}")

if __name__ == "__main__":
    main()

