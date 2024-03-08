Read ME!

docker build --tag myflask .


docker container run \
  --rm \
  --detach \
  --publish 127.0.0.1:5000:5000 \
  --env PICKLEJAR_ACCESS=${PICKLEJAR_ACCESS} \
  --env PICKLEJAR_SECRET=${PICKLEJAR_SECRET} \
  --name flask \
  myflask