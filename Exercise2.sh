#!/bin/bash

run_benchmark() {
	local model_id="$1"
	local tp=1
	if [ -n "$2" ]; then
		tp="$2"
	fi

	# &: start in background
	vllm serve "$model_id" --port 8080 -tp "$tp" &

 	# capture vllm background process
	VLLM_process=$!

	echo "Waiting for vLLM to start"

	# wait until curl successfully connects to the llm API
	while ! curl -s -f http://0.0.0.0:8080/v1/models > /dev/null; do
		sleep 2
	done

	echo "vLLM started. starting evaluation"
  
  # changed: agent type to our custom agent in order to test our agent
  # changed: removed nle test dataset
	python eval.py \
	agent.type=custom \
	agent.max_image_history=0 \
	agent.max_text_history=16 \
	eval.num_workers=4 \
	client.client_name=vllm \
	client.model_id="$model_id" \
	client.base_url=http://0.0.0.0:8080/v1 \
	envs.names="babyai-babaisai-textworld-crafter-minihack"

	# kill the vllm background process
	kill $VLLM_process

	echo "finished evaluation for $model_id"
}

# run selected models 
run_benchmark "Qwen/Qwen2.5-1.5B-Instruct"
run_benchmark "Qwen/Qwen2.5-3B-Instruct"
run_benchmark "Qwen/Qwen2.5-7B-Instruct"
