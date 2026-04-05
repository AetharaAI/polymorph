 omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297] 
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297]        █     █     █▄   ▄█
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.17.1rc1.dev126+gbc2c0c86e
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297]   █▄█▀ █     █     █     █  model   /models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:297] 
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:01 [utils.py:233] non-default args: {'model_tag': '/models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit', 'default_chat_template_kwargs': {'enable_thinking': False}, 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit', 'trust_remote_code': True, 'max_model_len': 16384, 'enforce_eager': True, 'served_model_name': ['omnicoder'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'gpu_memory_utilization': 0.53, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 6144, 'max_num_seqs': 8, 'enable_chunked_prefill': True}
omnicoder  | (APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [model.py:533] Resolved architecture: Qwen3_5ForConditionalGeneration
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [model.py:1580] Using max model len 16384
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [cache.py:211] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=6144.
omnicoder  | (APIServer pid=1) WARNING 03-17 07:16:07 [config.py:384] Mamba cache mode is set to 'align' for Qwen3_5ForConditionalGeneration by default when prefix caching is enabled
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [config.py:404] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [config.py:224] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [config.py:255] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [vllm.py:748] Asynchronous scheduling is enabled.
omnicoder  | (APIServer pid=1) WARNING 03-17 07:16:07 [vllm.py:782] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
omnicoder  | (APIServer pid=1) WARNING 03-17 07:16:07 [vllm.py:793] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [vllm.py:958] Cudagraph is disabled under eager mode
omnicoder  | (APIServer pid=1) INFO 03-17 07:16:07 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:20 [core.py:101] Initializing a V1 LLM engine (v0.17.1rc1.dev126+gbc2c0c86e) with config: model='/models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit', speculative_config=None, tokenizer='/models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=True, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=omnicoder, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['all'], 'splitting_ops': [], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [6144], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 0, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:21 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.4:50233 backend=nccl
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:21 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:27 [gpu_model_runner.py:4501] Starting to load model /models/llm/cyankiwi/OmniCoder-9B-AWQ-4bit...
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:27 [cuda.py:373] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:27 [mm_encoder_attention.py:230] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:27 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:27 [cuda.py:317] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
Loading safetensors checkpoint shards:   0% Completed | 0/3 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  33% Completed | 1/3 [00:01<00:02,  1.19s/it]
Loading safetensors checkpoint shards:  67% Completed | 2/3 [00:02<00:01,  1.17s/it]
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:02<00:00,  1.29it/s]
Loading safetensors checkpoint shards: 100% Completed | 3/3 [00:02<00:00,  1.13it/s]
omnicoder  | (EngineCore pid=164) 
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:30 [default_loader.py:293] Loading weights took 2.66 seconds
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:31 [gpu_model_runner.py:4584] Model loading took 8.41 GiB memory and 3.233857 seconds
omnicoder  | (EngineCore pid=164) INFO 03-17 07:16:31 [gpu_model_runner.py:5506] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
omnicoder  | (EngineCore pid=164) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
omnicoder  | (EngineCore pid=164)   return fn(*contiguous_args, **contiguous_kwargs)
omnicoder  | (EngineCore pid=164) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
omnicoder  | (EngineCore pid=164)   return fn(*contiguous_args, **contiguous_kwargs)
omnicoder  | (EngineCore pid=164) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
omnicoder  | (EngineCore pid=164)   return fn(*contiguous_args, **contiguous_kwargs)
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:03 [gpu_worker.py:452] Available KV cache memory: 13.11 GiB
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:03 [kv_cache_utils.py:1316] GPU KV cache size: 214,368 tokens
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:03 [kv_cache_utils.py:1321] Maximum concurrency for 16,384 tokens per request: 36.95x
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:04 [core.py:279] init engine (profile, create kv cache, warmup model) took 93.75 seconds
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:05 [vllm.py:748] Asynchronous scheduling is enabled.
omnicoder  | (EngineCore pid=164) WARNING 03-17 07:18:05 [vllm.py:782] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
omnicoder  | (EngineCore pid=164) WARNING 03-17 07:18:05 [vllm.py:793] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:05 [vllm.py:958] Cudagraph is disabled under eager mode
omnicoder  | (EngineCore pid=164) INFO 03-17 07:18:05 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:05 [api_server.py:569] Supported tasks: ['generate']
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:05 [parser_manager.py:202] "auto" tool choice has been enabled.
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:05 [parser_manager.py:202] "auto" tool choice has been enabled.
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:05 [base.py:180] Warming up chat template processing...
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:06 [hf.py:318] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:06 [base.py:186] Chat template warmup completed in 1.162s
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:06 [base.py:199] Warming up multi-modal processing...
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [base.py:213] Multi-modal warmup completed in 4.384s
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [parser_manager.py:202] "auto" tool choice has been enabled.
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [parser_manager.py:202] "auto" tool choice has been enabled.
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [api_server.py:573] Starting vLLM server on http://0.0.0.0:8000
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:36] Available routes are:
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /openapi.json, Methods: GET, HEAD
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /docs, Methods: GET, HEAD
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /docs/oauth2-redirect, Methods: GET, HEAD
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /redoc, Methods: GET, HEAD
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /tokenize, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /detokenize, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /load, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /version, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /health, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /metrics, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/models, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /ping, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /ping, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /invocations, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/chat/completions, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/responses, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/responses/{response_id}, Methods: GET
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/responses/{response_id}/cancel, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/completions, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/messages, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/messages/count_tokens, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /inference/v1/generate, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /scale_elastic_ep, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /is_scaling_elastic_ep, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/chat/completions/render, Methods: POST
omnicoder  | (APIServer pid=1) INFO 03-17 07:18:11 [launcher.py:45] Route: /v1/completions/render, Methods: POST
omnicoder  | (APIServer pid=1) INFO:     Started server process [1]
omnicoder  | (APIServer pid=1) INFO:     Waiting for application startup.
omnicoder  | (APIServer pid=1) INFO:     Application startup complete.
omnicoder  | (APIServer pid=1) INFO:     127.0.0.1:52084 - "GET /v1/models HTTP/1.1" 200 OK
omnicoder  | (APIServer pid=1) INFO:     127.0.0.1:57310 - "GET /v1/mo
 (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297] 
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297]        █     █     █▄   ▄█
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.17.1rc1.dev126+gbc2c0c86e
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297]   █▄█▀ █     █     █     █  model   /models/cyankiwi/Qwen3.5-9B-AWQ-4bit
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:297] 
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:21:59 [utils.py:233] non-default args: {'model_tag': '/models/cyankiwi/Qwen3.5-9B-AWQ-4bit', 'default_chat_template_kwargs': {'enable_thinking': False}, 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'api_key': ['EMPTY'], 'model': '/models/cyankiwi/Qwen3.5-9B-AWQ-4bit', 'trust_remote_code': True, 'max_model_len': 16384, 'enforce_eager': True, 'served_model_name': ['qwen3.5-9b'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'gpu_memory_utilization': 0.33, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 4096, 'max_num_seqs': 4, 'enable_chunked_prefill': True}
qwen3.5-9b  | (APIServer pid=1) The argument `trust_remote_code` is to be used with Auto classes. It has no effect here and is ignored.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [model.py:533] Resolved architecture: Qwen3_5ForConditionalGeneration
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [model.py:1580] Using max model len 16384
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [cache.py:211] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=4096.
qwen3.5-9b  | (APIServer pid=1) WARNING 03-17 07:22:05 [config.py:384] Mamba cache mode is set to 'align' for Qwen3_5ForConditionalGeneration by default when prefix caching is enabled
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [config.py:404] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [config.py:224] Setting attention block size to 1056 tokens to ensure that attention page size is >= mamba page size.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [config.py:255] Padding mamba page size by 0.76% to ensure that mamba page size and attention page size are exactly equal.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [vllm.py:748] Asynchronous scheduling is enabled.
qwen3.5-9b  | (APIServer pid=1) WARNING 03-17 07:22:05 [vllm.py:782] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
qwen3.5-9b  | (APIServer pid=1) WARNING 03-17 07:22:05 [vllm.py:793] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [vllm.py:958] Cudagraph is disabled under eager mode
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:22:05 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:18 [core.py:101] Initializing a V1 LLM engine (v0.17.1rc1.dev126+gbc2c0c86e) with config: model='/models/cyankiwi/Qwen3.5-9B-AWQ-4bit', speculative_config=None, tokenizer='/models/cyankiwi/Qwen3.5-9B-AWQ-4bit', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=True, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=qwen3.5-9b, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['all'], 'splitting_ops': [], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [4096], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.NONE: 0>, 'cudagraph_num_of_warmups': 0, 'cudagraph_capture_sizes': [], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 0, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:19 [parallel_state.py:1395] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.18.0.5:45015 backend=nccl
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:19 [parallel_state.py:1717] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:24 [gpu_model_runner.py:4501] Starting to load model /models/cyankiwi/Qwen3.5-9B-AWQ-4bit...
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:24 [cuda.py:373] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:24 [mm_encoder_attention.py:230] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:24 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:22:25 [cuda.py:317] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
Loading safetensors checkpoint shards:   0% Completed | 0/2 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  50% Completed | 1/2 [02:00<02:00, 120.66s/it]
Loading safetensors checkpoint shards: 100% Completed | 2/2 [02:52<00:00, 79.91s/it]
Loading safetensors checkpoint shards: 100% Completed | 2/2 [02:52<00:00, 86.02s/it]
qwen3.5-9b  | (EngineCore pid=129) 
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:25:17 [default_loader.py:293] Loading weights took 172.20 seconds
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:25:18 [gpu_model_runner.py:4584] Model loading took 8.41 GiB memory and 172.771411 seconds
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:25:18 [gpu_model_runner.py:5506] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-9b  | (EngineCore pid=129) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-9b  | (EngineCore pid=129)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-9b  | (EngineCore pid=129) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-9b  | (EngineCore pid=129)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-9b  | (EngineCore pid=129) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (16) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-9b  | (EngineCore pid=129)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:44 [gpu_worker.py:452] Available KV cache memory: 4.24 GiB
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:44 [kv_cache_utils.py:1316] GPU KV cache size: 68,640 tokens
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:44 [kv_cache_utils.py:1321] Maximum concurrency for 16,384 tokens per request: 11.91x
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:45 [core.py:279] init engine (profile, create kv cache, warmup model) took 87.24 seconds
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:45 [vllm.py:748] Asynchronous scheduling is enabled.
qwen3.5-9b  | (EngineCore pid=129) WARNING 03-17 07:26:45 [vllm.py:782] Enforce eager set, disabling torch.compile and CUDAGraphs. This is equivalent to setting -cc.mode=none -cc.cudagraph_mode=none
qwen3.5-9b  | (EngineCore pid=129) WARNING 03-17 07:26:45 [vllm.py:793] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:45 [vllm.py:958] Cudagraph is disabled under eager mode
qwen3.5-9b  | (EngineCore pid=129) INFO 03-17 07:26:45 [compilation.py:289] Enabled custom fusions: norm_quant, act_quant
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:45 [api_server.py:569] Supported tasks: ['generate']
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:46 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:46 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:46 [base.py:180] Warming up chat template processing...
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:47 [hf.py:318] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:47 [base.py:186] Chat template warmup completed in 1.386s
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:47 [base.py:199] Warming up multi-modal processing...
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [base.py:213] Multi-modal warmup completed in 4.491s
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [api_server.py:573] Starting vLLM server on http://0.0.0.0:8000
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:36] Available routes are:
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /openapi.json, Methods: GET, HEAD
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /docs, Methods: GET, HEAD
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /docs/oauth2-redirect, Methods: GET, HEAD
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /redoc, Methods: GET, HEAD
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /tokenize, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /detokenize, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /load, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /version, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /health, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /metrics, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/models, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /ping, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /ping, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /invocations, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/chat/completions, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/responses, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/responses/{response_id}, Methods: GET
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/responses/{response_id}/cancel, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/completions, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/messages, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/messages/count_tokens, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /inference/v1/generate, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /scale_elastic_ep, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /is_scaling_elastic_ep, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/chat/completions/render, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO 03-17 07:26:51 [launcher.py:45] Route: /v1/completions/render, Methods: POST
qwen3.5-9b  | (APIServer pid=1) INFO:     Started server process [1]
qwen3.5-9b  | (APIServer pid=1) INFO:     Waiting for application startup.
qwen3.5-9b  | (APIServer pid=1) INFO:     Application startup complete.

