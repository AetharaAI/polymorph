FROM node:20-alpine

WORKDIR /app/frontend

ENV NEXT_TELEMETRY_DISABLED=1

COPY frontend/package.json ./package.json
COPY frontend/pnpm-lock.yaml ./pnpm-lock.yaml
RUN npm install

COPY frontend/ ./
# Prevent container builds from inheriting local dev backend URL from .env.local.
RUN rm -f .env.local

ARG NEXT_PUBLIC_BACKEND_URL=http://localhost:38333
ENV NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL}

RUN npm run build

ENV NODE_ENV=production

EXPOSE 3000

CMD ["npm", "run", "start", "--", "-H", "0.0.0.0", "-p", "3000"]
