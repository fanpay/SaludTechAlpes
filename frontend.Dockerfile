FROM node:22.14.0

WORKDIR /app
EXPOSE 4200/
COPY ./src/frontend/ .
RUN npm install -g @angular/cli
RUN npm install
CMD [ "ng", "serve", "--host=0.0.0.0","--disable-host-check" ]
