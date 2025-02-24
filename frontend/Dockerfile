# Use a Node.js image based on Alpine
FROM node:16.20.0-alpine

# Set the working directory inside the container
WORKDIR /frontend

# Copy package.json and install the dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire frontend project
COPY . .

# Expose port 3000 for React
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
