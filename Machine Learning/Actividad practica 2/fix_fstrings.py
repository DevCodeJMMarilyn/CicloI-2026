import json
import re

file_path = 'jimenez_arias_actividad2.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            line_mod = line
            # Match print(f"...") or print(f'...')
            if 'print(f"' in line_mod or "print(f'" in line_mod:
                variables = re.findall(r'\{([^:]+)(?::\.[0-9]+f)?\}', line_mod)
                if variables:
                    # Replace {...} with %s
                    line_mod = re.sub(r'\{[^}]+\}', '%s', line_mod)
                    # Remove the 'f' prefix
                    line_mod = line_mod.replace('print(f"', 'print("').replace("print(f'", "print('")
                    
                    # Append the % (vars) before the closing parenthesis of print
                    # Example line: print("texto %s")\n
                    if line_mod.endswith('")\\n') or line_mod.endswith("')\\n"):
                        # Extract the quote type
                        quote = line_mod[-4] 
                        line_mod = line_mod[:-4] + quote + " % (" + ", ".join(variables) + "))\\n"
                    elif line_mod.endswith('")\n') or line_mod.endswith("')\n"):
                        quote = line_mod[-3] 
                        line_mod = line_mod[:-3] + quote + " % (" + ", ".join(variables) + "))\n"
                    elif line_mod.endswith('")') or line_mod.endswith("')"):
                        quote = line_mod[-2]
                        line_mod = line_mod[:-2] + quote + " % (" + ", ".join(variables) + "))"
            new_source.append(line_mod)
        cell['source'] = new_source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Fix applied to the notebook directly.")
