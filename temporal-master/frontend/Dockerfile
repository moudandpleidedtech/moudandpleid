FROM node:20-alpine

WORKDIR /app

# Install dependencies first (cached layer)
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

EXPOSE 3000

# Enable polling-based file watching for Docker volume mounts
ENV WATCHPACK_POLLING=true

CMD ["npm", "run", "dev"]
