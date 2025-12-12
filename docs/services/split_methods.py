import os
import re

services_dir = 'LoggerService'

for filename in os.listdir(services_dir):
    if not filename.endswith('.md'):
        continue

    input_path = os.path.join(services_dir, filename)
    base_name = os.path.splitext(filename)[0]
    output_dir = os.path.join(services_dir, base_name)
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Ներածություն section
    intro_match = re.search(r'(##\s+Ներածություն\b.*?)(?=^##\s+|\Z)', content, re.DOTALL | re.MULTILINE)
    intro_section = intro_match.group(1).strip() if intro_match else ''

    pattern = r'^###\s+(\w+)(.*?)(?=^###\s+\w+|\Z)'
    matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

    if not matches:
        print(f"⚠️ No methods or properties found in {filename}")
        continue

    print(f"📄 Processing {filename} ({len(matches)} items found)")

    method_table = ["## Մեթոդներ", "", "| Անվանում | Նկարագրություն |", "|----------|----------------|"]
    property_table = ["## Հատկություններ", "", "| Անվանում | Նկարագրություն |", "|----------|----------------|"]

    method_name_counts = {}  # To track overload numbering

    for method_name, desc in matches:
        desc_clean = desc.strip()

        # Extract signature (same as before)
        code_block_match = re.search(r'```c#\s*(public|private|internal|protected)?\s*[\w<>\[\]]+\s+(\w+)\s*\((.*?)\)', desc_clean, re.DOTALL)
        if code_block_match:
            params_str = code_block_match.group(3).strip()
            if params_str:
                param_types = []
                param_parts = re.split(r',(?![^<]*>)', params_str)
                for p in param_parts:
                    p = p.strip()
                    tokens = p.split()
                    tokens = [t for t in tokens if t not in ('ref', 'out', 'in', 'params')]
                    if len(tokens) >= 2:
                        param_type = ' '.join(tokens[:-1])
                    else:
                        param_type = tokens[0] if tokens else ''
                    param_types.append(param_type)
                param_types_str = ', '.join(param_types)
            else:
                param_types_str = ''
            signature = f"{method_name}({param_types_str})"
        else:
            param_types_str = ''
            signature = method_name

        suffix = "մեթոդ" if '(' in signature else "հատկություն"
        table = method_table if suffix == "մեթոդ" else property_table

        file_title = f"{base_name}.{signature} {suffix}"

        # Count occurrences for filenames
        count = method_name_counts.get(method_name, 0)
        method_name_counts[method_name] = count + 1

        if count == 0:
            filename_md = f"{method_name}.md"
        else:
            filename_md = f"{method_name}{count}.md"

        method_path = os.path.join(output_dir, filename_md)

        # Extract summary line
        lines = desc_clean.splitlines()
        in_code = False
        summary_line = '(առկա չէ նկարագրություն)'
        for line in lines:
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if not in_code and line.strip() and (line.strip().endswith(':') or line.strip().endswith('։')):
                summary_line = line.strip()
                break

        with open(method_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: {file_title}\n---\n\n")
            f.write(desc_clean + "\n")

        link = f"{base_name}/{filename_md}"
        table.append(f"| [{method_name}]({link}) | {summary_line} |")

    base_file_lines = [
        "---",
        f"title: {base_name} սերվիս",
        "---",
        ""
    ]
    if intro_section:
        base_file_lines.append(intro_section)
        base_file_lines.append("")

    if len(method_table) > 4:
        base_file_lines.extend(method_table)
        base_file_lines.append("")

    if len(property_table) > 4:
        base_file_lines.extend(property_table)

    with open(input_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(base_file_lines))

print("✅ Done processing all files.")
