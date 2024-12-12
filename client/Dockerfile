FROM node:23.2
WORKDIR /app
COPY . .
RUN yarn install
EXPOSE 5173
CMD ["yarn", "start:dev"]
