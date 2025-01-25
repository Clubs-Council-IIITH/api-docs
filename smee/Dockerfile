FROM node:20-slim

RUN npm install --global smee-client

CMD ["sh", "-c", "smee -u $SMEE_URL --target http://docs:8000/webhook"]