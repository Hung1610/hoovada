FROM nginx:stable-alpine

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

# Copy nginx configuration file.
RUN rm /etc/nginx/conf.d/*
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf


