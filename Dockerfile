FROM nodered/node-red:1.1.3
RUN npm install node-red-dashboard \
node-red-contrib-influxdb \
node-red-contrib-ambiclimate \
node-red-contrib-tplink \
node-red-contrib-iconv