FROM nginx:1.27-alpine

COPY frontend/public/index.html /usr/share/nginx/html/index.html
COPY frontend/assets /usr/share/nginx/html/assets

EXPOSE 80