FROM node

WORKDIR /app

COPY app/package*.json ./

RUN npm install

COPY app/. .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]