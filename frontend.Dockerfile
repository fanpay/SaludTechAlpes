# FROM node:22.14.0

# WORKDIR /app
# EXPOSE 4200/
# COPY ./src/frontend/ .
# RUN npm install -g @angular/cli
# RUN npm install
# CMD [ "ng", "serve", "--host=0.0.0.0","--disable-host-check" ]


FROM node:22.14.0-alpine AS BUILD
WORKDIR /build
COPY ./src/frontend/ .

RUN npm install

# COPY angular.json .
# COPY tailwind.config.js .
# COPY postcss.config.js .
# COPY tsconfig.json .
# COPY tsconfig.app.json .
# COPY tsconfig.spec.json .
# COPY src src

RUN npm run build:prod

FROM nginxinc/nginx-unprivileged:1.26.2-alpine3.20-perl
COPY --from=BUILD /build/dist/output/browser /usr/share/nginx/html
COPY --from=BUILD /build/nginx.conf /etc/nginx/nginx.conf
