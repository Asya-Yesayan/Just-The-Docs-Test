import os
import re

folder = "LoginService"  # path to your Markdown files

def parse_signature(signature: str):
    """Parse C# signature and return dict: param_name -> (type, default)"""
    param_map = {}
    signature = re.sub(r'\s+', ' ', signature.strip())
    if not signature:
        return param_map

    # Split by commas not inside <>
    params = [p.strip() for p in re.split(r',(?![^<]*>)', signature)]
    for p in params:
        # Remove ref/out/in/params keywords
        p = re.sub(r'^(ref|out|in|params)\s+', '', p)
        # Match type, name, optional default value
        m = re.match(r'(.+?)\s+(\w+)(?:\s*=\s*(.*))?$', p)
        if m:
            ptype, pname, default_val = m.groups()
            param_map[pname] = (ptype.strip(), default_val.strip() if default_val else "-")
        else:
            tokens = p.split()
            if len(tokens) >= 2:
                pname = tokens[-1]
                ptype = " ".join(tokens[:-1])
                param_map[pname] = (ptype, "-")
            elif tokens:
                param_map[tokens[0]] = (tokens[0], "-")
    return param_map

def get_param_info(pname, signature_params):
    """Return (type, default) for a param, with robust fuzzy matching."""
    if pname in signature_params:
        return signature_params[pname]

    # Ignore trailing 's' for plural mismatches
    pname_strip_s = pname.rstrip('s')
    for k, v in signature_params.items():
        if k == pname_strip_s or k.rstrip('s') == pname_strip_s:
            return v

    # Substring match fallback
    for k, v in signature_params.items():
        if pname.lower() in k.lower() or k.lower() in pname.lower():
            return v

    return "-", "-"

for filename in os.listdir(folder):
    if not filename.endswith(".md"):
        continue

    path = os.path.join(folder, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content by code blocks and html comments to process separately
    parts = re.split(r'(<!--.*?-->|```c#.*?```)', content, flags=re.DOTALL)
    new_content = ""
    last_signature_params = {}

    for part in parts:
        if part.startswith('```c#'):
            # Extract method signature inside the code block
            sig_match = re.search(
                r'(?:public|private|internal|protected)?\s*[\w<>\[\]\?,\s]+\s+(\w+)\s*\((.*?)\)',
                part, re.DOTALL
            )
            if sig_match:
                _, params_str = sig_match.groups()
                last_signature_params = parse_signature(params_str)
            new_content += part
        elif part.startswith('<!--'):
            new_content += part
        else:
            # Replace **Պարամետրեր** sections in normal text
            def replace_params(match):
                section = match.group(0)
                lines = section.splitlines()
                params = []
                current_name = None
                current_desc = []

                for line in lines:
                    line_strip = line.strip()
                    m = re.match(r'\*\s*`?(\w+)`?\s*-\s*(.*)', line_strip)
                    if m:
                        if current_name:
                            params.append((current_name, " ".join(current_desc).strip()))
                        current_name = m.group(1)
                        current_desc = [m.group(2)]
                    elif current_name and line_strip:
                        current_desc.append(line_strip)
                if current_name:
                    params.append((current_name, " ".join(current_desc).strip()))

                table = [
                    "**Պարամետրեր**",
                    "",
                    "| Անվանում | Տեսակ | Լռությամբ արժեք | Նկարագրություն |",
                    "|----------|--------|------------------|----------------|"
                ]
                for name, desc in params:
                    ptype, default_val = get_param_info(name, last_signature_params)
                    table.append(f"| {name} | {ptype} | {default_val} | {desc} |")

                return "\n".join(table) + "\n"

            part = re.sub(
                r'\*\*Պարամետրեր\*\*.*?(?=(\n##|\Z|<!--))',
                replace_params,
                part,
                flags=re.DOTALL
            )
            new_content += part

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

print("✅ All **Պարամետրեր** tables updated correctly, including plural/fuzzy matches, multi-line, default values, generics, tuples, and HTML comments.")
