taching to qwen3.5-122
qwen3.5-122    | WARNING 03-01 11:10:58 [argparse_utils.py:193] With `vllm serve`, you should provide the model as a positional argument or in a config file instead of via the `--model` option. The `--model` option will be removed in v0.13.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293] 
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293]        █     █     █▄   ▄█
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.16.1rc1.dev111+gafd089f23
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293]   █▄█▀ █     █     █     █  model   /models
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:293] 
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:10:58 [utils.py:229] non-default args: {'model_tag': '/models', 'enable_auto_tool_choice': True, 'tool_call_parser': 'qwen3_coder', 'host': '0.0.0.0', 'port': 8001, 'model': '/models', 'max_model_len': 131072, 'served_model_name': ['qwen3.5-122'], 'generation_config': 'vllm', 'reasoning_parser': 'qwen3', 'tensor_parallel_size': 2, 'disable_custom_all_reduce': True, 'swap_space': 8.0, 'kv_cache_dtype': 'fp8', 'enable_prefix_caching': True, 'max_num_batched_tokens': 8192, 'max_num_seqs': 6, 'enable_chunked_prefill': True}
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [model.py:532] Resolved architecture: Qwen3_5MoeForConditionalGeneration
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [model.py:1557] Using max model len 131072
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [cache.py:223] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=8192.
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 11:11:05 [config.py:373] Mamba cache mode is set to 'align' for Qwen3_5MoeForConditionalGeneration by default when prefix caching is enabled
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [config.py:393] Warning: Prefix caching in Mamba cache 'align' mode is currently enabled. Its support for Mamba layers is experimental. Please report any issues you may observe.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [config.py:536] Setting attention block size to 4176 tokens to ensure that attention page size is >= mamba page size.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [config.py:567] Padding mamba page size by 0.19% to ensure that mamba page size and attention page size are exactly equal.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:11:05 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:11:18 [core.py:101] Initializing a V1 LLM engine (v0.16.1rc1.dev111+gafd089f23) with config: model='/models', speculative_config=None, tokenizer='/models', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=131072, download_dir=None, load_format=auto, tensor_parallel_size=2, pipeline_parallel_size=1, data_parallel_size=1, disable_custom_all_reduce=True, quantization=compressed-tensors, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_fallback=False, disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='qwen3', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=qwen3.5-122, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'level': None, 'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_split_points': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 8, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
qwen3.5-122    | (EngineCore_DP0 pid=246) WARNING 03-01 11:11:18 [multiproc_executor.py:945] Reducing Torch parallelism from 30 threads to 1 to avoid unnecessary CPU contention. Set OMP_NUM_THREADS in the external environment to tune this value as needed.
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:11:18 [multiproc_executor.py:134] DP group leader: node_rank=0, node_rank_within_dp=0, master_addr=127.0.0.1, mq_connect_ip=172.18.0.4 (local), world_size=2, local_world_size=2
qwen3.5-122    | (Worker pid=313) INFO 03-01 11:11:25 [parallel_state.py:1394] world_size=2 rank=1 local_rank=1 distributed_init_method=tcp://127.0.0.1:50831 backend=nccl
qwen3.5-122    | (Worker pid=312) INFO 03-01 11:11:25 [parallel_state.py:1394] world_size=2 rank=0 local_rank=0 distributed_init_method=tcp://127.0.0.1:50831 backend=nccl
qwen3.5-122    | (Worker pid=312) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
qwen3.5-122    | (Worker pid=313) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
qwen3.5-122    | (Worker pid=312) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
qwen3.5-122    | (Worker pid=313) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
qwen3.5-122    | (Worker pid=312) INFO 03-01 11:11:25 [pynccl.py:111] vLLM is using nccl==2.27.5
qwen3.5-122    | (Worker pid=312) WARNING 03-01 11:11:26 [symm_mem.py:67] SymmMemCommunicator: Device capability 8.9 not supported, communicator is not available.
qwen3.5-122    | (Worker pid=313) WARNING 03-01 11:11:26 [symm_mem.py:67] SymmMemCommunicator: Device capability 8.9 not supported, communicator is not available.
qwen3.5-122    | (Worker pid=313) INFO 03-01 11:11:26 [parallel_state.py:1716] rank 1 in world size 2 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 1, EP rank 1, EPLB rank N/A
qwen3.5-122    | (Worker pid=312) INFO 03-01 11:11:26 [parallel_state.py:1716] rank 0 in world size 2 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0, EPLB rank N/A
qwen3.5-122    | (Worker pid=313) INFO 03-01 11:11:32 [base.py:106] Offloader set to NoopOffloader
qwen3.5-122    | (Worker pid=312) INFO 03-01 11:11:32 [base.py:106] Offloader set to NoopOffloader
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [gpu_model_runner.py:4202] Starting to load model /models...
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [cuda.py:453] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [mm_encoder_attention.py:213] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:11:32 [cuda.py:453] Using backend AttentionBackendEnum.FLASH_ATTN for vit attention
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:11:32 [mm_encoder_attention.py:213] Using AttentionBackendEnum.FLASH_ATTN for MMEncoderAttention.
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [compressed_tensors_moe.py:199] Using CompressedTensorsWNA16MarlinMoEMethod
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [compressed_tensors_moe.py:1266] Using Marlin backend for WNA16 MoE (group_size=32, num_bits=4)
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:11:32 [compressed_tensors_moe.py:199] Using CompressedTensorsWNA16MarlinMoEMethod
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:11:32 [cuda.py:405] Using FLASHINFER attention backend out of potential backends: ['FLASHINFER', 'TRITON_ATTN'].
Loading safetensors checkpoint shards:   0% Completed | 0/15 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   7% Completed | 1/15 [00:43<10:15, 43.99s/it]
Loading safetensors checkpoint shards:  13% Completed | 2/15 [01:55<13:00, 60.03s/it]
Loading safetensors checkpoint shards:  20% Completed | 3/15 [03:22<14:30, 72.53s/it]
Loading safetensors checkpoint shards:  27% Completed | 4/15 [04:45<14:01, 76.49s/it]
Loading safetensors checkpoint shards:  33% Completed | 5/15 [06:12<13:25, 80.51s/it]
Loading safetensors checkpoint shards:  40% Completed | 6/15 [07:53<13:05, 87.33s/it]
Loading safetensors checkpoint shards:  47% Completed | 7/15 [09:19<11:34, 86.80s/it]
Loading safetensors checkpoint shards:  53% Completed | 8/15 [11:02<10:44, 92.12s/it]
Loading safetensors checkpoint shards:  60% Completed | 9/15 [11:05<06:25, 64.27s/it]
Loading safetensors checkpoint shards:  67% Completed | 10/15 [11:08<03:46, 45.39s/it]
Loading safetensors checkpoint shards:  73% Completed | 11/15 [11:11<02:09, 32.44s/it]
Loading safetensors checkpoint shards:  80% Completed | 12/15 [11:14<01:10, 23.52s/it]
Loading safetensors checkpoint shards:  87% Completed | 13/15 [11:17<00:34, 17.28s/it]
Loading safetensors checkpoint shards:  93% Completed | 14/15 [11:20<00:12, 12.98s/it]
Loading safetensors checkpoint shards: 100% Completed | 15/15 [11:22<00:00,  9.59s/it]
Loading safetensors checkpoint shards: 100% Completed | 15/15 [11:22<00:00, 45.51s/it]
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) 
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:22:55 [default_loader.py:293] Loading weights took 682.77 seconds
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:22:58 [gpu_model_runner.py:4285] Model loading took 36.73 GiB memory and 684.785983 seconds
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:22:58 [gpu_model_runner.py:5207] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:22:58 [gpu_model_runner.py:5207] Encoder cache will be initialized with a budget of 16384 tokens, and profiled with 1 image items of the maximum feature size.
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:10 [backends.py:916] Using cache directory: /root/.cache/vllm/torch_compile_cache/505b3217a9/rank_0_0/backbone for vLLM's torch.compile
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:10 [backends.py:976] Dynamo bytecode transform time: 6.90 s
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:14 [backends.py:350] Cache the graph of compile range (1, 8192) for later use
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:23:14 [backends.py:350] Cache the graph of compile range (1, 8192) for later use
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:23:36 [decorators.py:580] saving AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/cf954d3b2df674c32986177c69304f29ae153d4b060fd6eab37bc3eae5febeeb/rank_1_0/model
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:36 [backends.py:366] Compiling a graph for compile range (1, 8192) takes 24.99 s
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:36 [monitor.py:35] torch.compile takes 33.07 s in total
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:36 [decorators.py:580] saving AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/cf954d3b2df674c32986177c69304f29ae153d4b060fd6eab37bc3eae5febeeb/rank_0_0/model
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) INFO 03-01 11:23:36 [decorators.py:588] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/cf954d3b2df674c32986177c69304f29ae153d4b060fd6eab37bc3eae5febeeb/rank_1_0/model
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:36 [decorators.py:588] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/cf954d3b2df674c32986177c69304f29ae153d4b060fd6eab37bc3eae5febeeb/rank_0_0/model
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:38 [gpu_worker.py:423] Available KV cache memory: 1.73 GiB
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:23:38 [kv_cache_utils.py:1314] GPU KV cache size: 75,168 tokens
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:23:38 [kv_cache_utils.py:1319] Maximum concurrency for 131,072 tokens per request: 1.89x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 4/4 [00:00<00:00,  4.84it/s]
Capturing CUDA graphs (decode, FULL): 100%|██████████| 3/3 [00:02<00:00,  1.29it/s]
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) INFO 03-01 11:23:42 [gpu_model_runner.py:5313] Graph capturing finished in 4 secs, took 0.69 GiB
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:23:42 [core.py:282] init engine (profile, create kv cache, warmup model) took 44.51 seconds
qwen3.5-122    | (EngineCore_DP0 pid=246) INFO 03-01 11:23:49 [vllm.py:747] Asynchronous scheduling is enabled.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:49 [api_server.py:495] Supported tasks: ['generate']
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:49 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:49 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:49 [serving.py:185] Warming up chat template processing...
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [hf.py:318] Detected the chat template content format to be 'string'. You can set `--chat-template-content-format` to override this.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [serving.py:210] Chat template warmup completed in 1236.2ms
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [parser_manager.py:202] "auto" tool choice has been enabled.
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [api_server.py:500] Starting vLLM API server 0 on http://0.0.0.0:8001
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:38] Available routes are:
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /openapi.json, Methods: GET, HEAD
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /docs, Methods: GET, HEAD
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /docs/oauth2-redirect, Methods: GET, HEAD
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /redoc, Methods: GET, HEAD
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /tokenize, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /detokenize, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /load, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /version, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /health, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /metrics, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/models, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /ping, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /ping, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /invocations, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/chat/completions, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/chat/completions/render, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/responses, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/responses/{response_id}, Methods: GET
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/responses/{response_id}/cancel, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/completions, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/completions/render, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /v1/messages, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /inference/v1/generate, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /scale_elastic_ep, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO 03-01 11:23:51 [launcher.py:47] Route: /is_scaling_elastic_ep, Methods: POST
qwen3.5-122    | (APIServer pid=1) INFO:     Started server process [1]
qwen3.5-122    | (APIServer pid=1) INFO:     Waiting for application startup.
qwen3.5-122    | (APIServer pid=1) INFO:     Application startup complete.
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 12:04:29 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (APIServer pid=1) INFO 03-01 12:05:21 [loggers.py:259] Engine 000: Avg prompt throughput: 2.3 tokens/s, Avg generation throughput: 26.1 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.3:55542 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 12:05:31 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 12.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 12:05:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 12:09:23 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (19) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (19) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.3:41690 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 12:09:31 [loggers.py:259] Engine 000: Avg prompt throughput: 1.9 tokens/s, Avg generation throughput: 51.2 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 12:09:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:29:22 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (26) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (26) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:29:31 [loggers.py:259] Engine 000: Avg prompt throughput: 2.6 tokens/s, Avg generation throughput: 67.4 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:29:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 77.2 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:29:51 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 77.1 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:30:01 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 77.1 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:41910 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:30:11 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 75.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:30:21 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:33:41 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:01 [loggers.py:259] Engine 000: Avg prompt throughput: 5.3 tokens/s, Avg generation throughput: 13.4 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:11 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.9 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:21 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.7 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:31 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.8 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.7 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:34:51 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.6 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:41556 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:35:01 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 12.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:35:11 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:48:06 [protocol.py:51] The following fields were present in the request but ignored: {'supports_reasoning', 'supports_function_calling', 'model_group', 'supports_images', 'supports_vision'}
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:48:11 [loggers.py:259] Engine 000: Avg prompt throughput: 5.5 tokens/s, Avg generation throughput: 40.6 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:48:21 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.1 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:57880 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:48:31 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 3.3 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:48:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:50:22 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:50:22 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (APIServer pid=1) The channel dimension is ambiguous. Got image shape torch.Size([3, 1, 1]). Assuming channels are the first dimension. Use the [input_data_format](https://huggingface.co/docs/transformers/main/internal/image_processing_utils#transformers.image_transforms.rescale.input_data_format) parameter to assign the channel dimension.
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:60750 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:60740 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:50:31 [loggers.py:259] Engine 000: Avg prompt throughput: 12.3 tokens/s, Avg generation throughput: 10.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%, MM cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:50:41 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%, MM cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:50:43 [protocol.py:51] The following fields were present in the request but ignored: {'model_group', 'supports_images', 'supports_reasoning', 'supports_vision', 'supports_function_calling'}
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:38020 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) WARNING 03-01 14:50:43 [protocol.py:51] The following fields were present in the request but ignored: {'supports_vision', 'model_group', 'supports_function_calling', 'supports_images', 'supports_reasoning'}
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=313) (Worker_TP1 pid=313)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312) /usr/local/lib/python3.12/dist-packages/vllm/model_executor/layers/fla/ops/utils.py:113: UserWarning: Input tensor shape suggests potential format mismatch: seq_len (23) < num_heads (32). This may indicate the inputs were passed in head-first format [B, H, T, ...] when head_first=False was specified. Please verify your input tensor format matches the expected shape [B, T, H, ...].
qwen3.5-122    | (Worker pid=312) (Worker_TP0 pid=312)   return fn(*contiguous_args, **contiguous_kwargs)
qwen3.5-122    | (APIServer pid=1) INFO:     172.18.0.2:38024 - "POST /v1/chat/completions HTTP/1.1" 200 OK
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:50:51 [loggers.py:259] Engine 000: Avg prompt throughput: 6.8 tokens/s, Avg generation throughput: 68.5 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 0.0%, MM cache hit rate: 0.0%
qwen3.5-122    | (APIServer pid=1) INFO 03-01 14:51:01 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 17.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%, MM cache hit rate: 0.0%
qwen3.5-122    | (APIServer p