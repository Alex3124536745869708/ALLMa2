import json
from pathlib import Path


E1_results = ["2026-10-05_16-39-31_naive_Qwen_Qwen2.5-0.5B-Instruct",
"2026-10-05_17-22-57_naive_Qwen_Qwen2.5-1.5B-Instruct",
"2026-10-06_11-46-04_naive_Qwen_Qwen2.5-14B-Instruct",
"2026-10-06_14-48-37_naive_Qwen_Qwen2.5-3B-Instruct",
"2026-10-06_16-02-23_naive_Qwen_Qwen2.5-7B-Instruct",
"2026-10-06_17-51-00_naive_gemma-4-31b-it"]

# performance matrix (LLM x Benchmarks)
matrix = dict()

results_path = Path("results")

for result in E1_results:
    result_path = results_path / result
    model = result_path.name.split("_")[-1]

    with open(result_path / "summary.json", "r") as f:
        summary = json.loads(f.read())

    for name, metrics in summary["environments"].items():
        prev = matrix.get(model, dict())
        prev[name] = (metrics["progression_percentage"], metrics["standard_error"])
        matrix[model] = prev

# create the latex table
out = r"""\begin{table}[t]
\caption{Average progress in percentage of different LLM models and sizes on the BALROG benchmark.}
\label{tab:performance_matrix}
\vskip 0.15in
\centering
\resizebox{0.6\textwidth}{!}{%
\begin{tabular}{l|c|c|c|c|c|c}
\hline
"""
benchmarks = ["BabyAI", "Crafter", "TextWorld", "BabaIsAI", "MiniHack", "nle"]
models = ["Qwen2.5-0.5B-Instruct", "Qwen2.5-1.5B-Instruct", "Qwen2.5-3B-Instruct", "Qwen2.5-7B-Instruct", "Qwen2.5-14B-Instruct", "gemma-4-31b-it"]
out += "models & " + " & ".join(benchmarks) + r" \\" + "\n"
out += r"\hline" + "\n"
for model in models:
    results = ["$" + str(round(matrix[model][bench.lower()][0], 2)) + "\pm" + str(round(matrix[model][bench.lower()][1], 2)) + "$" for bench in benchmarks]
    out += model + " & " + " & ".join(results) + r" \\" + "\n"
out += r"""\hline
\end{tabular}%
}
\end{table}
"""
with open("performance_matrix.tex", "w") as f:
    f.write(out)