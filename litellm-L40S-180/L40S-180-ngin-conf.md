user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 4096;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;

    # --- Upstreams ---
    # LiteLLM gateway (OpenAI-compatible router)
    upstream litellm_gateway {
        server 127.0.0.1:4000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }
    # Voice Gateway (FastAPI – port 8005)
    upstream voice_gateway {
        server 127.0.0.1:8005;
        keepalive 32;
    }



    # BlacBoxAudio API (FastAPI / Uvicorn)
    upstream blackbox_api {
        server 127.0.0.1:8004;
        keepalive 32;
    }

    # Maya TTS API
    upstream maya_tts {
        server 127.0.0.1:8003;
        keepalive 32;
    }


    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;

    # ---------------------------
    # HTTP -> HTTPS redirect
    # ---------------------------
    server {
        listen 80;
        listen [::]:80;
        server_name api.blackboxaudio.tech;

        return 301 https://$host$request_uri;
    }

    # ---------------------------
    # HTTPS (origin)
    # ---------------------------
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name api.blackboxaudio.tech;

        # Certbot paths (adjust if yours differ)
        ssl_certificate     /etc/letsencrypt/live/api.blackboxaudio.tech/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.blackboxaudio.tech/privkey.pem;
        
        client_max_body_size 100M;
        client_body_timeout 300s;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # OpenAI-compatible chat completions (LiteLLM)
        location ^~ /v1/chat/ {
            proxy_pass http://litellm_gateway;
            proxy_http_version 1.1;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Authorization $http_authorization;

            proxy_buffering off;
            proxy_cache off;
        }
        # --------------------------------------------------
        # VOICE API (FastAPI – port 8004)
        # --------------------------------------------------

        # TTS endpoints
        location = /health {
            proxy_pass http://blackbox_api;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Connection "";
            proxy_buffering off;
        }

        # ASR endpoints (supports streaming / websockets)
        location ^~ /v1/asr/ {
            proxy_pass http://blackbox_api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_buffering off;
        }

        # Voice API health (public)
        location = /v1/health {
            proxy_pass http://blackbox_api;
            access_log off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Voice API key admin endpoint (auth)
        location ^~ /v1/admin/ {
            proxy_pass http://blackbox_api;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Authorization $http_authorization;
            proxy_buffering off;
            proxy_cache off;
        }

        # Voice auth + usage endpoints (auth)
        location ^~ /v1/auth/ {
             proxy_pass http://blackbox_api;
             proxy_http_version 1.1;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Authorization $http_authorization;
             proxy_buffering off;
             proxy_cache off;
        }

        # Voice TTS Supports Streming (v1/tts/stream / v1/tts/clone)
        location ^~ /v1/tts/ {
             proxy_pass http://blackbox_api;
             proxy_http_version 1.1;
             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection "upgrade";
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Authorization $http_authorization;
             proxy_buffering off;
            
        }
        # Voice Gateway API (port 8005)
        location ^~ /v1/voice/ {
             proxy_pass http://voice_gateway;
             proxy_http_version 1.1;

             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

             # Needed for audio uploads + streaming
             client_max_body_size 200M;
             proxy_buffering off;
        }



        # Voice auth + usage endpoints (auth)
        location ^~ /api/v1/webhooks/stripe {
             proxy_pass http://blackbox_api;
             proxy_http_version 1.1;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Authorization $http_authorization;
             proxy_buffering off;
             proxy_cache off;
        }

        # Usage Metering
        location = /v1/usage {
             proxy_pass http://blackbox_api;
             proxy_http_version 1.1;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Authorization $http_authorization;
             proxy_buffering off;
             proxy_cache off;
        }

        # Pricing is public (voice API)
        location = /v1/pricing {
             proxy_pass http://blackbox_api;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Maya TTS (Text → Speech)
        location ^~ /api/v1/speak {
             proxy_pass http://maya_tts;
             proxy_http_version 1.1;

             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

             proxy_buffering off;
             proxy_read_timeout 3600;
        }

        location ^~ /api/v1/speak/sync {
             proxy_pass http://maya_tts;
             proxy_http_version 1.1;

             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

             proxy_buffering off;
             proxy_cache off;
         }

         location = /api/v1/health {
             access_log off;
             proxy_pass http://maya_tts/health;
         }

         


        # --------------------------------------------------
        # LiteLLM API (Qwen3-Omni Reasoning Multi-Modal Model)
        # --------------------------------------------------

        # Models Routes Through LiteLLM
        location = /v1/models {
            limit_req zone=api_limit burst=50 nodelay;
            
            proxy_pass http://litellm_gateway;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Authorization $http_authorization;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_cache off;
        }
        #
        # LiteLLM UI (dashboard on port 4000)
        #
        location /litellm/ui {
            proxy_pass http://litellm_gateway/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Connection "";
            proxy_buffering off;
        }


        # Health check
        location /health {
            access_log off;
            proxy_pass http://litellm_gateway/health;
            proxy_set_header Authorization $http_authorization;
        }

        # Main API endpoint - routes through LiteLLM
        # Qwen3-30B-Omni-Thinking
        location = /v1/chat/completions {
            proxy_pass http://litellm_gateway;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Authorization $http_authorization;
            proxy_set_header Connection "";
            proxy_buffering off;
            proxy_cache off;

        }

        # Status page
        location / {
            add_header Content-Type text/html;
            return 200 '<html><body><h1>BlackBoxAudio API</h1><p>Status: ONLINE</p><ul><li>/v1/tts/* -> API</li><li>/v1/asr/* -> API</li><li>/v1/chat/completions -> LiteLLM</li></ul></body></html>';
        }
    }
}
ubuntu@l40s-180-us-west-or-1:~/aether-model-node/control/litellm$ 

