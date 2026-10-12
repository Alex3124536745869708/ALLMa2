#!/bin/bash

run_api_benchmark() {
	local client_name="$1"
	local model_id="$2"

	python eval.py \
		agent.type=customEx3 \
		agent.max_image_history=0 \
		agent.max_text_history=16 \
		eval.num_workers=16 \
		client.client_name="$client_name" \
		client.model_id="$model_id" \
                envs.names=babyai-babaisai-crafter
}

# run_api_benchmark "gemini" "gemini-3.8-flash"
# run_api_benchmark "gemini" "gemma-4-31b-it"
run_api_benchmark "gemini" "gemini-3.8-live"
# run_api_benchmark "gemini" "gemini-3.8-live-extended-thinking"
