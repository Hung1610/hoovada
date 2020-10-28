FROM nginx:stable-alpine

# Copy nginx configuration file.
RUN rm /etc/nginx/conf.d/*

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

ENV TZ=Asia/Ho_Chi_Minh

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime 

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]