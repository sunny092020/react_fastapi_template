FROM node:18
WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn
RUN yarn global add eslint
COPY . .
EXPOSE 3000
