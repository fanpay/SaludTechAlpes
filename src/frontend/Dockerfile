FROM node:22.14.0-alpine AS BUILD
WORKDIR /build

COPY package.json .
RUN npm install

COPY angular.json .
COPY tailwind.config.js .
COPY postcss.config.js .
COPY tsconfig.json .
COPY tsconfig.app.json .
COPY tsconfig.spec.json .
COPY src src

RUN npm run build:prod

FROM nginxinc/nginx-unprivileged:1.26.2-alpine3.20-perl
COPY --from=BUILD /build/dist/output/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
