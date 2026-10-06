uv python pin 3.10
uv run python -m venv .venv
source .venv/bin/activate
pip install -e .
balrog-post-install
pip install vllm
module load CUDA/12.9.1
export CUDA_HOME=$(dirname $(dirname $(which nvcc)))