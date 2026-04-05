erver pid=1)              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/workspace/vllm/vllm/renderers/mistral.py", line 40, in safe_apply_chat_template
(APIServer pid=1)     raise ValueError(str(e)) from e
(APIServer pid=1) ValueError: Tool call id was call_1 but must be a-z, A-Z, 0-9, with a length of 9.
(APIServer pid=1) INFO:     172.18.0.1:55266 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 13:08:37 [loggers.py:259] Engine 000: Avg prompt throughput: 5.2 tokens/s, Avg generation throughput: 3.3 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 4.6%
(APIServer pid=1) INFO 03-19 13:08:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 4.6%
(APIServer pid=1) INFO:     172.18.0.1:44364 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 13:36:27 [loggers.py:259] Engine 000: Avg prompt throughput: 256.7 tokens/s, Avg generation throughput: 6.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 3.8%
(APIServer pid=1) INFO 03-19 13:36:37 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 3.8%
(APIServer pid=1) INFO:     172.18.0.1:58204 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:58204 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 13:38:07 [loggers.py:259] Engine 000: Avg prompt throughput: 463.3 tokens/s, Avg generation throughput: 10.9 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 12.3%
(APIServer pid=1) INFO:     172.18.0.1:36432 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     172.18.0.1:36432 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO 03-19 13:38:17 [loggers.py:259] Engine 000: Avg prompt throughput: 193.6 tokens/s, Avg generation throughput: 4.2 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 24.0%
(APIServer pid=1) INFO:     172.18.0.1:38858 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO:     172.18.0.1:38868 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO:     172.18.0.1:38878 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO:     172.18.0.1:38884 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO:     172.18.0.1:38896 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
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
(APIServer pid=1) mistral_common.exceptions.InvalidMessageStructureException: Unexpected role 'tool' after role 'user'
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
(APIServer pid=1) ValueError: Unexpected role 'tool' after role 'user'
(APIServer pid=1) INFO 03-19 13:38:27 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 24.0%
(APIServer pid=1) WARNING 03-19 13:38:29 [mistral.py:110] Truncating tool call ID: call_a7def9754be148438669115d to 38669115d
(APIServer pid=1) WARNING 03-19 13:38:29 [mistral.py:124] Truncating tool_call_id: call_a7def9754be148438669115d to 38669115d
(APIServer pid=1) INFO:     172.18.0.1:57554 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) WARNING 03-19 13:38:32 [mistral.py:110] Truncating tool call ID: call_a7def9754be148438669115d to 38669115d
(APIServer pid=1) WARNING 03-19 13:38:32 [mistral.py:124] Truncating tool_call_id: call_a7def9754be148438669115d to 38669115d
(APIServer pid=1) INFO:     172.18.0.1:57554 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO 03-19 13:38:37 [loggers.py:259] Engine 000: Avg prompt throughput: 78.8 tokens/s, Avg generation throughput: 12.1 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 38.4%
(APIServer pid=1) INFO 03-19 13:38:47 [loggers.py:259] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 38.4%



