FROM node:alpine3.15

WORKDIR /app

COPY ./package.json ./

RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm", "run", "start"]