import json
import traceback
import matplotlib.pyplot as plt

plt.ion() # Prevent show() from blocking

with open("jimenez_arias_actividad2.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

global_vars = {'display': print}
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        code = "".join(cell["source"])
        if code.strip():
            try:
                exec(code, global_vars)
            except Exception as e:
                print(f"Error in cell index {i}: {e}")
                print("Code was:")
                print(code)
                traceback.print_exc()
                exit(1)
print("All code cells tested successfully!")
