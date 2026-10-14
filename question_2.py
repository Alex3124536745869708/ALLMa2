import json
from pathlib import Path


E2_results = ["2026-10-08_19-05-18_custom_Qwen_Qwen2.5-1.5B-Instruct",
"2026-10-08_19-19-41_custom_Qwen_Qwen2.5-3B-Instruct",
"2026-10-08_19-31-27_custom_Qwen_Qwen2.5-7B-Instruct",
"2026-10-12_13-55-20_custom_gemma-4-31b-it"]

# performance matrix (LLM x Benchmarks)
matrix = dict()

results_path = Path("results")

for result in E2_results:
    result_path = results_path / result
    model = result_path.name.split("_")[-1]

    with open(result_path / "summary.json", "r") as f:
        summary = json.loads(f.read())

    for name, metrics in summary["environments"].items():
        prev = matrix.get(model, dict())
        prev[name] = metrics["progression_percentage"]
        matrix[model] = prev

# create the latex table
out = r"""\begin{table}[t]
\caption{Average progress in percentage of different LLM models and sizes on the BALROG benchmark with Zero-shot-CoT, Meta prompting, and planning.}
\label{tab:performance_matrix2}
\vskip 0.15in
\centering
\resizebox{0.6\textwidth}{!}{%
\begin{tabular}{l|c|c|c}
\hline
"""
benchmarks = ["BabyAI", "Crafter", "BabaIsAI"]
models = ["Qwen2.5-1.5B-Instruct", "Qwen2.5-3B-Instruct", "Qwen2.5-7B-Instruct", "gemma-4-31b-it"]
out += "models & " + " & ".join(benchmarks) + r" \\" + "\n"
out += r"\hline" + "\n"
for model in models:
    results = [str(round(matrix[model][bench.lower()], 3)) for bench in benchmarks]
    out += model + " & " + " & ".join(results) + r" \\" + "\n"
out += r"""\hline
\end{tabular}%
}
\end{table}
"""
with open("performance_matrix2.tex", "w") as f:
    f.write(out)