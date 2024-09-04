FROM node:22-slim AS build-client

WORKDIR /app

COPY client/package.json client/package-lock.json .

RUN npm install

COPY client .

RUN npm run build


FROM jonasal/nginx-certbot:5.4-alpine

# The nginx base image will envsubst the template with env variables at runtime and place
# it at /etc/nginx/conf.d/concrexit.conf. See https://registry.hub.docker.com/_/nginx/.
COPY infra/nginx/diyivi.conf.template /etc/nginx/templates/diyivi.conf.template

COPY --from=build-client /app/dist /client/dist