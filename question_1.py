import json
from pathlib import Path
from pprint import pprint

# performance matrix (LLM x Benchmarks)
matrix = dict()

results_path = Path("results")

for result in results_path.iterdir():
    model = "_".join(result.name.split("_")[4:])

    with open(result / "summary.json", "r") as f:
        summary = json.loads(f.read())

    for name, metrics in summary["environments"].items():
        prev = matrix.get(model, dict())
        prev[name] = metrics["progression_percentage"]
        matrix[model] = prev

# create the latex table
out = r"""\begin{table}[t]
\caption{}
\label{tab:performance_matrix}
\vskip 0.15in
\centering
\begin{tabular}{c|c|c|c|c|c}
\hline
"""
benchmarks = ["BabyAI", "Crafter", "TextWorld", "BabaIsAI", "MiniHack", "nle"]
models = ["Qwen2.5-0.5B-Instruct", "Qwen2.5-1.5B-Instruct", "Qwen2.5-3B-Instruct", "Qwen2.5-7B-Instruct", "Qwen2.5-14B-Instruct"]
out += " & ".join(benchmarks) + r" \\" + "\n"
for model in models:
    results = [str(round(matrix[model][bench.lower()], 3)) for bench in benchmarks]
    out += model + " & " + " & ".join(results) + r" \\" + "\n"
out += r"""\hline
\end{tabular}
\end{table}
"""
with open("performance_matrix.tex", "w") as f:
    f.write(out)