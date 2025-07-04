FROM node:20

WORKDIR /app

COPY package.json package-lock.json ./

# Clean install to avoid native rollup
RUN npm install 

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
