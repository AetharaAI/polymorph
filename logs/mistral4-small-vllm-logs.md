ubuntu@l40s-180-us-west-or-1:~$ docker logs -f mistral4-small
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297] 
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297]        █     █     █▄   ▄█
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.0.0
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297]   █▄█▀ █     █     █     █  model   /models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:297] 
(APIServer pid=1) INFO 03-19 06:21:23 [utils.py:233] non-default args: {'model_tag': '/models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit', 'enable_auto_tool_choice': True, 'tool_call_parser': 'mistral', 'host': '0.0.0.0', 'model': '/models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit', 'max_model_len': 32768, 'served_model_name': ['mistral4-small'], 'tensor_parallel_size': 2, 'gpu_memory_utilization': 0.82, 'max_num_batched_tokens': 4096, 'max_num_seqs': 2}
(APIServer pid=1) Unrecognized keys in `rope_parameters` for 'rope_type'='yarn': {'apply_yarn_scaling'}
(APIServer pid=1) `rope_parameters`'s factor field must be a float >= 1, got 128
(APIServer pid=1) `rope_parameters`'s beta_fast field must be a float, got 32
(APIServer pid=1) `rope_parameters`'s beta_slow field must be a float, got 1
(APIServer pid=1) Unrecognized keys in `rope_parameters` for 'rope_type'='yarn': {'apply_yarn_scaling'}
(APIServer pid=1) `rope_parameters`'s factor field must be a float >= 1, got 128
(APIServer pid=1) `rope_parameters`'s beta_fast field must be a float, got 32
(APIServer pid=1) `rope_parameters`'s beta_slow field must be a float, got 1
(APIServer pid=1) INFO 03-19 06:21:31 [model.py:533] Resolved architecture: PixtralForConditionalGeneration
(APIServer pid=1) INFO 03-19 06:21:31 [model.py:1582] Using max model len 32768
(APIServer pid=1) INFO 03-19 06:21:31 [scheduler.py:231] Chunked prefill is enabled with max_num_batched_tokens=4096.
(APIServer pid=1) INFO 03-19 06:21:31 [vllm.py:754] Asynchronous scheduling is enabled.
(APIServer pid=1) [2026-03-19 06:21:31] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
(APIServer pid=1) [2026-03-19 06:21:32] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
(APIServer pid=1) [2026-03-19 06:21:33] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
(EngineCore pid=235) INFO 03-19 06:21:40 [core.py:103] Initializing a V1 LLM engine (v0.0.0) with config: model='/models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit', speculative_config=None, tokenizer='/models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=2, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=compressed-tensors, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False), seed=0, served_model_name=mistral4-small, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'splitting_ops': ['vllm::unified_attention', 'vllm::unified_attention_with_output', 'vllm::unified_mla_attention', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::gdn_attention_core', 'vllm::olmo_hybrid_gdn_full_forward', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'compile_sizes': [], 'compile_ranges_endpoints': [4096], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False}, 'max_cudagraph_capture_size': 4, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': True, 'static_all_moe_layers': []}
(EngineCore pid=235) WARNING 03-19 06:21:40 [multiproc_executor.py:997] Reducing Torch parallelism from 30 threads to 1 to avoid unnecessary CPU contention. Set OMP_NUM_THREADS in the external environment to tune this value as needed.
(EngineCore pid=235) INFO 03-19 06:21:40 [multiproc_executor.py:134] DP group leader: node_rank=0, node_rank_within_dp=0, master_addr=127.0.0.1, mq_connect_ip=172.18.0.2 (local), world_size=2, local_world_size=2
[2026-03-19 06:21:47] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
[2026-03-19 06:21:47] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
(Worker pid=301) INFO 03-19 06:21:47 [parallel_state.py:1395] world_size=2 rank=0 local_rank=0 distributed_init_method=tcp://127.0.0.1:44291 backend=nccl
(Worker pid=302) INFO 03-19 06:21:48 [parallel_state.py:1395] world_size=2 rank=1 local_rank=1 distributed_init_method=tcp://127.0.0.1:44291 backend=nccl
(Worker pid=301) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
(Worker pid=302) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
(Worker pid=301) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
(Worker pid=302) <frozen importlib._bootstrap_external>:1301: FutureWarning: The cuda.nvrtc module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.nvrtc module instead.
(Worker pid=301) INFO 03-19 06:21:48 [pynccl.py:111] vLLM is using nccl==2.27.5
(Worker pid=301) WARNING 03-19 06:21:48 [symm_mem.py:67] SymmMemCommunicator: Device capability 8.9 not supported, communicator is not available.
(Worker pid=302) WARNING 03-19 06:21:48 [symm_mem.py:67] SymmMemCommunicator: Device capability 8.9 not supported, communicator is not available.
(Worker pid=302) WARNING 03-19 06:21:48 [custom_all_reduce.py:165] Custom allreduce is disabled because your platform lacks GPU P2P capability or P2P test failed. To silence this warning, specify disable_custom_all_reduce=True explicitly.
(Worker pid=301) WARNING 03-19 06:21:48 [custom_all_reduce.py:165] Custom allreduce is disabled because your platform lacks GPU P2P capability or P2P test failed. To silence this warning, specify disable_custom_all_reduce=True explicitly.
(Worker pid=302) INFO 03-19 06:21:48 [parallel_state.py:1717] rank 1 in world size 2 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 1, EP rank 1, EPLB rank N/A
(Worker pid=301) INFO 03-19 06:21:48 [parallel_state.py:1717] rank 0 in world size 2 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0, EPLB rank N/A
(Worker_TP0 pid=301) INFO 03-19 06:21:49 [gpu_model_runner.py:4492] Starting to load model /models/cyankiwi/Mistral-Small-4-119B-2603-AWQ-4bit...
(Worker_TP1 pid=302) INFO 03-19 06:21:50 [vllm.py:754] Asynchronous scheduling is enabled.
(Worker_TP1 pid=302) INFO 03-19 06:21:50 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [vllm.py:754] Asynchronous scheduling is enabled.
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [compressed_tensors_wNa16.py:112] Using MarlinLinearKernel for CompressedTensorsWNA16
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [cuda.py:317] Using TRITON_MLA attention backend out of potential backends: ['TRITON_MLA'].
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [mla_attention.py:2137] Using FlashAttention prefill for MLA
(Worker_TP1 pid=302) INFO 03-19 06:21:50 [compressed_tensors_moe.py:191] Using CompressedTensorsWNA16MarlinMoEMethod
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [compressed_tensors_moe.py:191] Using CompressedTensorsWNA16MarlinMoEMethod
(Worker_TP0 pid=301) INFO 03-19 06:21:50 [compressed_tensors_moe.py:1175] Using Marlin backend for WNA16 MoE (group_size=32, num_bits=4)
Loading safetensors checkpoint shards:   0% Completed | 0/14 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   7% Completed | 1/14 [02:55<37:56, 175.08s/it]
Loading safetensors checkpoint shards:  14% Completed | 2/14 [06:16<38:05, 190.47s/it]
Loading safetensors checkpoint shards:  21% Completed | 3/14 [09:06<33:11, 181.08s/it]
Loading safetensors checkpoint shards:  29% Completed | 4/14 [12:31<31:45, 190.51s/it]
Loading safetensors checkpoint shards:  36% Completed | 5/14 [15:44<28:44, 191.61s/it]
Loading safetensors checkpoint shards:  43% Completed | 6/14 [19:04<25:55, 194.50s/it]
Loading safetensors checkpoint shards:  50% Completed | 7/14 [22:19<22:42, 194.61s/it]
Loading safetensors checkpoint shards:  57% Completed | 8/14 [25:35<19:29, 194.94s/it]
Loading safetensors checkpoint shards:  64% Completed | 9/14 [28:46<16:09, 193.87s/it]
Loading safetensors checkpoint shards:  71% Completed | 10/14 [30:49<11:27, 171.76s/it]
Loading safetensors checkpoint shards:  79% Completed | 11/14 [33:29<08:24, 168.28s/it]
Loading safetensors checkpoint shards:  86% Completed | 12/14 [36:18<05:37, 168.52s/it]
Loading safetensors checkpoint shards:  93% Completed | 13/14 [38:15<02:32, 152.87s/it]
Loading safetensors checkpoint shards: 100% Completed | 14/14 [38:56<00:00, 119.24s/it]
Loading safetensors checkpoint shards: 100% Completed | 14/14 [38:56<00:00, 166.93s/it]
(Worker_TP0 pid=301) 
(Worker_TP0 pid=301) INFO 03-19 07:00:47 [default_loader.py:314] Loading weights took 2337.04 seconds
(Worker_TP0 pid=301) INFO 03-19 07:00:49 [gpu_model_runner.py:4577] Model loading took 33.94 GiB memory and 2338.305738 seconds
(Worker_TP1 pid=302) INFO 03-19 07:00:49 [gpu_model_runner.py:5499] Encoder cache will be initialized with a budget of 4096 tokens, and profiled with 1 image items of the maximum feature size.
(Worker_TP0 pid=301) INFO 03-19 07:00:49 [gpu_model_runner.py:5499] Encoder cache will be initialized with a budget of 4096 tokens, and profiled with 1 image items of the maximum feature size.
(Worker_TP0 pid=301) INFO 03-19 07:00:58 [backends.py:988] Using cache directory: /root/.cache/vllm/torch_compile_cache/ad95a4b8d1/rank_0_0/backbone for vLLM's torch.compile
(Worker_TP0 pid=301) INFO 03-19 07:00:58 [backends.py:1048] Dynamo bytecode transform time: 7.58 s
(Worker_TP0 pid=301) INFO 03-19 07:01:04 [backends.py:371] Cache the graph of compile range (1, 4096) for later use
(Worker_TP1 pid=302) INFO 03-19 07:01:04 [backends.py:371] Cache the graph of compile range (1, 4096) for later use
(Worker_TP0 pid=301) INFO 03-19 07:01:09 [backends.py:387] Compiling a graph for compile range (1, 4096) takes 11.00 s
(Worker_TP0 pid=301) INFO 03-19 07:01:11 [decorators.py:627] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/08927529080deb59e153026253d32f966a84d0bed8c36b3bbd6233422b7cab54/rank_0_0/model
(Worker_TP0 pid=301) INFO 03-19 07:01:11 [monitor.py:48] torch.compile took 21.37 s in total
(Worker_TP0 pid=301) /usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP0 pid=301) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP0 pid=301) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP0 pid=301) important use case and you want to speed it up with online
(Worker_TP0 pid=301) softmax.
(Worker_TP0 pid=301) 
(Worker_TP0 pid=301)   warnings.warn(
(Worker_TP1 pid=302) /usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP1 pid=302) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP1 pid=302) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP1 pid=302) important use case and you want to speed it up with online
(Worker_TP1 pid=302) softmax.
(Worker_TP1 pid=302) 
(Worker_TP1 pid=302)   warnings.warn(
(Worker_TP0 pid=301) INFO 03-19 07:01:15 [monitor.py:76] Initial profiling/warmup run took 4.16 s
(Worker_TP0 pid=301) INFO 03-19 07:01:16 [kv_cache_utils.py:826] Overriding num_gpu_blocks=0 with num_gpu_blocks_override=4
(Worker_TP0 pid=301) WARNING 03-19 07:01:16 [gpu_model_runner.py:6050] CUDAGraphMode.FULL_AND_PIECEWISE is not supported with TritonMLABackend backend (support: AttentionCGSupport.NEVER); setting cudagraph_mode=PIECEWISE because attention is compiled piecewise
(Worker_TP0 pid=301) INFO 03-19 07:01:16 [gpu_model_runner.py:5618] Profiling CUDA graph memory: PIECEWISE=3 (largest=4)
(Worker_TP1 pid=302) INFO 03-19 07:01:16 [kv_cache_utils.py:826] Overriding num_gpu_blocks=0 with num_gpu_blocks_override=4
(Worker_TP1 pid=302) WARNING 03-19 07:01:16 [gpu_model_runner.py:6050] CUDAGraphMode.FULL_AND_PIECEWISE is not supported with TritonMLABackend backend (support: AttentionCGSupport.NEVER); setting cudagraph_mode=PIECEWISE because attention is compiled piecewise
(Worker_TP1 pid=302) INFO 03-19 07:01:16 [gpu_model_runner.py:5618] Profiling CUDA graph memory: PIECEWISE=3 (largest=4)
(Worker_TP0 pid=301) /usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP0 pid=301) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP0 pid=301) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP0 pid=301) important use case and you want to speed it up with online
(Worker_TP0 pid=301) softmax.
(Worker_TP0 pid=301) 
(Worker_TP0 pid=301)   warnings.warn(
(Worker_TP1 pid=302) /usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP1 pid=302) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP1 pid=302) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP1 pid=302) important use case and you want to speed it up with online
(Worker_TP1 pid=302) softmax.
(Worker_TP1 pid=302) 
(Worker_TP1 pid=302)   warnings.warn(
(Worker_TP0 pid=301) INFO 03-19 07:01:20 [gpu_model_runner.py:5697] Estimated CUDA graph memory: 0.14 GiB total
(Worker_TP1 pid=302) INFO 03-19 07:01:20 [gpu_model_runner.py:5697] Estimated CUDA graph memory: 0.14 GiB total
(Worker_TP0 pid=301) INFO 03-19 07:01:21 [gpu_worker.py:452] Available KV cache memory: 1.63 GiB
(Worker_TP0 pid=301) INFO 03-19 07:01:21 [gpu_worker.py:486] In v0.19, CUDA graph memory profiling will be enabled by default (VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=1), which more accurately accounts for CUDA graph memory during KV cache allocation. To try it now, set VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=1 and increase --gpu-memory-utilization from 0.8200 to 0.8232 to maintain the same effective KV cache size.
(Worker_TP1 pid=302) INFO 03-19 07:01:21 [gpu_worker.py:486] In v0.19, CUDA graph memory profiling will be enabled by default (VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=1), which more accurately accounts for CUDA graph memory during KV cache allocation. To try it now, set VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=1 and increase --gpu-memory-utilization from 0.8200 to 0.8232 to maintain the same effective KV cache size.
(EngineCore pid=235) INFO 03-19 07:01:21 [kv_cache_utils.py:1316] GPU KV cache size: 75,776 tokens
(EngineCore pid=235) INFO 03-19 07:01:21 [kv_cache_utils.py:1321] Maximum concurrency for 32,768 tokens per request: 2.31x
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):   0%|          | 0/3 [0Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  33%|███▎      | 1/3 [0Capturing CUDA graphs (mixed prefill-decode, PIECEWISE):  67%|██████▋   | 2/3 [00:00<00:00,  4.04it/s]/usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP0 pid=301) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP0 pid=301) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP0 pid=301) important use case and you want to speed it up with online
(Worker_TP0 pid=301) softmax.
(Worker_TP0 pid=301) 
(Worker_TP0 pid=301)   warnings.warn(
(Worker_TP1 pid=302) /usr/local/lib/python3.12/dist-packages/torch/_inductor/lowering.py:7627: UserWarning: 
(Worker_TP1 pid=302) Online softmax is disabled on the fly since Inductor decides to
(Worker_TP1 pid=302) split the reduction. Cut an issue to PyTorch if this is an
(Worker_TP1 pid=302) important use case and you want to speed it up with online
(Worker_TP1 pid=302) softmax.
(Worker_TP1 pid=302) 
(Worker_TP1 pid=302)   warnings.warn(
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 3/3 [0Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|██████████| 3/3 [00:01<00:00,  1.56it/s]
(Worker_TP0 pid=301) INFO 03-19 07:01:24 [gpu_model_runner.py:5757] Graph capturing finished in 3 secs, took 0.07 GiB
(Worker_TP0 pid=301) INFO 03-19 07:01:24 [gpu_worker.py:614] CUDA graph pool memory: 0.07 GiB (actual), 0.14 GiB (estimated), difference: 0.07 GiB (105.7%).
(Worker_TP1 pid=302) INFO 03-19 07:01:24 [gpu_worker.py:614] CUDA graph pool memory: 0.07 GiB (actual), 0.14 GiB (estimated), difference: 0.07 GiB (105.7%).
(EngineCore pid=235) INFO 03-19 07:01:24 [core.py:281] init engine (profile, create kv cache, warmup model) took 35.41 seconds
(EngineCore pid=235) [2026-03-19 07:01:24] INFO tekken.py:204: Non special vocabulary size is 130072 with 1000 special tokens.
(EngineCore pid=235) INFO 03-19 07:01:26 [vllm.py:754] Asynchronous scheduling is enabled.
(APIServer pid=1) INFO 03-19 07:01:26 [api_server.py:573] Supported tasks: ['generate']
(APIServer pid=1) INFO 03-19 07:01:26 [parser_manager.py:202] "auto" tool choice has been enabled.
(APIServer pid=1) INFO 03-19 07:01:26 [parser_manager.py:202] "auto" tool choice has been enabled.
(APIServer pid=1) INFO 03-19 07:01:26 [parser_manager.py:202] "auto" tool choice has been enabled.
(APIServer pid=1) INFO 03-19 07:01:26 [base.py:216] Multi-modal warmup completed in 0.199s
(APIServer pid=1) INFO 03-19 07:01:26 [parser_manager.py:202] "auto" tool choice has been enabled.
(APIServer pid=1) INFO 03-19 07:01:26 [api_server.py:577] Starting vLLM server on http://0.0.0.0:8000
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:37] Available routes are:
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /openapi.json, Methods: HEAD, GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /docs, Methods: HEAD, GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /docs/oauth2-redirect, Methods: HEAD, GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /redoc, Methods: HEAD, GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /tokenize, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /detokenize, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /load, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /version, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /health, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /metrics, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/models, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /ping, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /ping, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /invocations, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/chat/completions, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/responses, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/responses/{response_id}, Methods: GET
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/responses/{response_id}/cancel, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/completions, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/messages, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/messages/count_tokens, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /scale_elastic_ep, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /is_scaling_elastic_ep, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/chat/completions/render, Methods: POST
(APIServer pid=1) INFO 03-19 07:01:26 [launcher.py:46] Route: /v1/completions/render, Methods: POST
(APIServer pid=1) INFO:     Started server process [1]
(APIServer pid=1) INFO:     Waiting for application startup.
(APIServer pid=1) INFO:     Application startup complete.
(APIServer pid=1) ERROR 03-19 07:05:38 [serving.py:215] Error with model error=ErrorInfo(message='The model `qwen3.5-122` does not exist.', type='NotFoundError', param='model', code=404)
(APIServer pid=1) INFO:     172.18.0.1:50300 - "POST /v1/chat/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     172.18.0.1:43494 - "GET /v1/models HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:37950 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:08:57 [loggers.py:259] Engine 000: Avg prompt throughput: 2.3 tokens/s, Avg generation throughput: 0.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
(APIServer pid=1) INFO 03-19 07:09:07 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
(APIServer pid=1) INFO:     172.18.0.1:45030 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:11:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.7 tokens/s, Avg generation throughput: 0.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 34.8%
(APIServer pid=1) INFO 03-19 07:11:57 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 34.8%
(APIServer pid=1) INFO:     172.18.0.1:58138 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:12:27 [loggers.py:259] Engine 000: Avg prompt throughput: 2.7 tokens/s, Avg generation throughput: 3.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 21.9%
(APIServer pid=1) INFO 03-19 07:12:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 21.9%
(APIServer pid=1) INFO:     172.18.0.1:51910 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:15:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.8 tokens/s, Avg generation throughput: 0.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 33.0%
(APIServer pid=1) INFO:     172.18.0.1:38208 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:15:57 [loggers.py:259] Engine 000: Avg prompt throughput: 2.8 tokens/s, Avg generation throughput: 5.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 25.6%
(APIServer pid=1) INFO:     172.18.0.1:39744 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:16:07 [loggers.py:259] Engine 000: Avg prompt throughput: 3.2 tokens/s, Avg generation throughput: 3.8 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 20.4%
(APIServer pid=1) INFO 03-19 07:16:17 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 20.4%
(APIServer pid=1) INFO:     172.18.0.1:51502 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:16:27 [loggers.py:259] Engine 000: Avg prompt throughput: 3.0 tokens/s, Avg generation throughput: 13.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 17.1%
(APIServer pid=1) INFO:     172.18.0.1:41556 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:16:37 [loggers.py:259] Engine 000: Avg prompt throughput: 4.0 tokens/s, Avg generation throughput: 8.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 14.1%
(APIServer pid=1) INFO 03-19 07:16:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 14.1%
(APIServer pid=1) INFO:     172.18.0.1:56852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:56852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:37:07 [loggers.py:259] Engine 000: Avg prompt throughput: 3.6 tokens/s, Avg generation throughput: 4.8 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 21.7%
(APIServer pid=1) INFO:     172.18.0.1:56852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:56852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:37:17 [loggers.py:259] Engine 000: Avg prompt throughput: 4.6 tokens/s, Avg generation throughput: 10.7 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 25.7%
(APIServer pid=1) INFO:     172.18.0.1:56852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:37:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.8 tokens/s, Avg generation throughput: 10.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 31.0%
(APIServer pid=1) INFO 03-19 07:37:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 31.0%
(APIServer pid=1) ERROR 03-19 07:44:47 [serving.py:215] Error with model error=ErrorInfo(message='The model `qwen3.5-122` does not exist.', type='NotFoundError', param='model', code=404)
(APIServer pid=1) INFO:     172.18.0.1:59302 - "POST /v1/chat/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     172.18.0.1:34614 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:45:17 [loggers.py:259] Engine 000: Avg prompt throughput: 4.0 tokens/s, Avg generation throughput: 0.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 28.3%
(APIServer pid=1) INFO 03-19 07:45:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 28.3%
(APIServer pid=1) INFO:     172.18.0.1:45274 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:45:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.8 tokens/s, Avg generation throughput: 0.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 32.5%
(APIServer pid=1) INFO 03-19 07:45:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 32.5%
(APIServer pid=1) INFO:     172.18.0.1:48472 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:45:57 [loggers.py:259] Engine 000: Avg prompt throughput: 2.5 tokens/s, Avg generation throughput: 1.8 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 33.0%
(APIServer pid=1) INFO 03-19 07:46:07 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 33.0%
(APIServer pid=1) INFO:     172.18.0.1:55422 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:54:17 [loggers.py:259] Engine 000: Avg prompt throughput: 10.2 tokens/s, Avg generation throughput: 1.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 29.4%
(APIServer pid=1) INFO 03-19 07:54:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 29.4%
(APIServer pid=1) INFO:     172.18.0.1:34808 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:55:17 [loggers.py:259] Engine 000: Avg prompt throughput: 0.6 tokens/s, Avg generation throughput: 1.6 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 39.5%
(APIServer pid=1) INFO 03-19 07:55:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 39.5%
(APIServer pid=1) INFO:     172.18.0.1:53446 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:56:17 [loggers.py:259] Engine 000: Avg prompt throughput: 0.6 tokens/s, Avg generation throughput: 2.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 46.8%
(APIServer pid=1) INFO 03-19 07:56:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 46.8%
(APIServer pid=1) INFO:     172.18.0.1:52160 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 07:57:47 [loggers.py:259] Engine 000: Avg prompt throughput: 6.9 tokens/s, Avg generation throughput: 5.8 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 44.4%
(APIServer pid=1) INFO 03-19 07:57:57 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 44.4%
(APIServer pid=1) INFO:     172.18.0.1:50700 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:46756 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:46768 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:46782 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:46786 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:46790 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:24 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:24 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:46794 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:25 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:25 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:55600 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:26 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:26 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:55610 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:27 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:27 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:55626 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:28 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:28 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:55630 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:29 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:29 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) INFO:     172.18.0.1:55634 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:33 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:33 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:33 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:33 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:55638 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:55644 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:34 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:55660 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:36 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:36 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:36 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:36 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:45486 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:37 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:37 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:37 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:37 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:45488 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:38 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:38 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:38 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:38 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) INFO:     172.18.0.1:45504 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:42 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:45508 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:43 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:45520 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:44 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:45526 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:45 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:35102 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:46 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:35104 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:110] Truncating tool call ID: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:124] Truncating tool_call_id: call_a8b485a5d2214be195f08aa9 to 195f08aa9
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:110] Truncating tool call ID: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:124] Truncating tool_call_id: call_e6195bc07fe3442d82d3b430 to d82d3b430
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:110] Truncating tool call ID: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) WARNING 03-19 10:20:47 [mistral.py:124] Truncating tool_call_id: call_0f12021eebce4d53b05988a5 to 3b05988a5
(APIServer pid=1) INFO:     172.18.0.1:35116 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:56408 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:56408 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO:     172.18.0.1:43434 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO 03-19 10:26:17 [loggers.py:259] Engine 000: Avg prompt throughput: 2.7 tokens/s, Avg generation throughput: 3.2 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 43.2%
(APIServer pid=1) INFO:     172.18.0.1:43440 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 193, in render_chat
(APIServer pid=1)     _mt.validate_request_params(request)
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 213, in validate_request_params
(APIServer pid=1)     raise ValueError("chat_template is not supported for Mistral tokenizers.")
(APIServer pid=1) ValueError: chat_template is not supported for Mistral tokenizers.
(APIServer pid=1) INFO 03-19 10:26:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 43.2%
(APIServer pid=1) INFO:     172.18.0.1:39232 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 10:26:37 [loggers.py:259] Engine 000: Avg prompt throughput: 6.9 tokens/s, Avg generation throughput: 3.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 40.4%
(APIServer pid=1) INFO 03-19 10:26:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 40.4%
(APIServer pid=1) INFO:     172.18.0.1:43986 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 10:27:37 [loggers.py:259] Engine 000: Avg prompt throughput: 1.1 tokens/s, Avg generation throughput: 3.2 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 40.9%
(APIServer pid=1) INFO 03-19 10:27:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 40.9%
(APIServer pid=1) INFO:     172.18.0.1:48446 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 12:50:27 [loggers.py:259] Engine 000: Avg prompt throughput: 265.7 tokens/s, Avg generation throughput: 5.7 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 11.9%
(APIServer pid=1) INFO 03-19 12:50:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 11.9%
(APIServer pid=1) INFO:     172.18.0.1:52470 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 12:52:07 [loggers.py:259] Engine 000: Avg prompt throughput: 322.3 tokens/s, Avg generation throughput: 5.8 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 6.6%
(APIServer pid=1) INFO 03-19 12:52:17 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 6.6%
(APIServer pid=1) INFO:     172.18.0.1:40432 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:40432 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO:     172.18.0.1:40232 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO:     172.18.0.1:40248 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO 03-19 12:54:27 [loggers.py:259] Engine 000: Avg prompt throughput: 332.3 tokens/s, Avg generation throughput: 1.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 4.6%
(APIServer pid=1) INFO:     172.18.0.1:40250 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO:     172.18.0.1:40266 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO:     172.18.0.1:40276 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) INFO 03-19 12:54:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 4.6%
(APIServer pid=1) WARNING 03-19 12:54:49 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:49 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:56724 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:54:50 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:50 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:56732 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:54:52 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:52 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:56746 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:54:54 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:54 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:56750 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:54:55 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:55 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:56760 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:54:56 [mistral.py:110] Truncating tool call ID: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) WARNING 03-19 12:54:56 [mistral.py:124] Truncating tool_call_id: call_4a9e6f3765804f14b0343bb3 to 4b0343bb3
(APIServer pid=1) INFO:     172.18.0.1:41510 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:02 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:02 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:41524 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:03 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:03 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:41532 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:05 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:05 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:41540 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:06 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:06 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:59670 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:07 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:07 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:59686 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:08 [mistral.py:110] Truncating tool call ID: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) WARNING 03-19 12:55:08 [mistral.py:124] Truncating tool_call_id: call_052758cc3c354b478b3d42bc to 78b3d42bc
(APIServer pid=1) INFO:     172.18.0.1:59692 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:21 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:21 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:36288 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:22 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:22 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:36290 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:23 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:23 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:36300 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:24 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:24 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:36304 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:25 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:25 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:45332 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
(APIServer pid=1) WARNING 03-19 12:55:26 [mistral.py:110] Truncating tool call ID: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) WARNING 03-19 12:55:26 [mistral.py:124] Truncating tool_call_id: call_3a5ce08d7c964d83825d8cd6 to 3825d8cd6
(APIServer pid=1) INFO:     172.18.0.1:45334 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=1) ERROR:    Exception in ASGI application
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 34, in safe_apply_chat_template
(APIServer pid=1)     return tokenizer.apply_chat_template(messages, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/tokenizers/mistral.py", line 466, in apply_chat_template
(APIServer pid=1)     return self.transformers_tokenizer.apply_chat_template(
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/transformers/tokenization_mistral_common.py", line 1190, in apply_chat_template
(APIServer pid=1)     tokenized_request = self.tokenizer.encode_chat_completion(chat_request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/tokens/tokenizers/mistral.py", line 374, in encode_chat_completion
(APIServer pid=1)     validated_request = self._chat_completion_request_validator.validate_request(request)
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 121, in validate_request
(APIServer pid=1)     self.validate_messages(request.messages, continue_final_message=request.continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 97, in validate_messages
(APIServer pid=1)     self._validate_message_list_structure(messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 449, in _validate_message_list_structure
(APIServer pid=1)     super()._validate_message_list_structure(messages=messages, continue_final_message=continue_final_message)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 326, in _validate_message_list_structure
(APIServer pid=1)     self._validate_message_order(messages)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/mistral_common/protocol/instruct/validator.py", line 277, in _validate_message_order
(APIServer pid=1)     raise InvalidMessageStructureException(
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'user' after role 'tool'
(APIServer pid=1) 
(APIServer pid=1) The above exception was the direct cause of the following exception:
(APIServer pid=1) 
(APIServer pid=1) Traceback (most recent call last):
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
(APIServer pid=1)     result = await app(  # type: ignore[func-returns-value]
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
(APIServer pid=1)     return await self.app(scope, receive, send)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/applications.py", line 1160, in __call__
(APIServer pid=1)     await super().__call__(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/applications.py", line 107, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 186, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/errors.py", line 164, in __call__
(APIServer pid=1)     await self.app(scope, receive, _send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/cors.py", line 87, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 177, in __call__
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/prometheus_fastapi_instrumentator/middleware.py", line 175, in __call__
(APIServer pid=1)     await self.app(scope, receive, send_wrapper)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/middleware/exceptions.py", line 63, in __call__
(APIServer pid=1)     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 716, in __call__
(APIServer pid=1)     await self.middleware_stack(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 736, in app
(APIServer pid=1)     await route.handle(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/routing.py", line 290, in handle
(APIServer pid=1)     await self.app(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 130, in app
(APIServer pid=1)     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 53, in wrapped_app
(APIServer pid=1)     raise exc
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/starlette/_exception_handler.py", line 42, in wrapped_app
(APIServer pid=1)     await app(scope, receive, sender)
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 116, in app
(APIServer pid=1)     response = await f(request)
(APIServer pid=1)                ^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 670, in app
(APIServer pid=1)     raw_response = await run_endpoint_function(
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/fastapi/routing.py", line 324, in run_endpoint_function
(APIServer pid=1)     return await dependant.call(**values)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 95, in wrapper
(APIServer pid=1)     return handler_task.result()
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/utils.py", line 116, in wrapper
(APIServer pid=1)     return await func(*args, **kwargs)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/api_router.py", line 55, in create_chat_completion
(APIServer pid=1)     generator = await handler.create_chat_completion(request, raw_request)
(APIServer pid=1)                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 261, in create_chat_completion
(APIServer pid=1)     result = await self.render_chat_request(request)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/openai/chat_completion/serving.py", line 224, in render_chat_request
(APIServer pid=1)     return await self.openai_serving_render.render_chat(request)
(APIServer pid=1)            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 242, in render_chat
(APIServer pid=1)     conversation, engine_prompts = await self._preprocess_chat(
(APIServer pid=1)                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/entrypoints/serve/render/serving.py", line 528, in _preprocess_chat
(APIServer pid=1)     (conversation,), (engine_prompt,) = await renderer.render_chat_async(
(APIServer pid=1)                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/base.py", line 817, in render_chat_async
(APIServer pid=1)     for conv, prompt in await asyncio.gather(*rendered):
(APIServer pid=1)                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 125, in render_messages_async
(APIServer pid=1)     prompt_raw = await self._apply_chat_template_async(
(APIServer pid=1)                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/lib/python3.12/concurrent/futures/thread.py", line 59, in run
(APIServer pid=1)     result = self.fn(*self.args, **self.kwargs)
(APIServer pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Unexpected role 'user' after role 'tool'
^Cubuntu@l40s-180-us-west-or-1:~$ 

