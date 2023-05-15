# 如果log目录不存在
if [ ! -d "log" ]; then
printf "log dir not exist, create it\n"
mkdir log
touch log/unit.log
touch log/access.log
fi
if [ ! -d "state" ]; then
printf "state dir not exist, create it\n"
mkdir state
fi

printf "start unit\n"
export UNIT=$(                                                         \
      docker run -d                                                      \
      --mount type=bind,src="$(pwd)/config/",dst=/docker-entrypoint.d/   \
      --mount type=bind,src="$(pwd)/log/unit.log",dst=/var/log/unit.log  \
      --mount type=bind,src="$(pwd)/log/access.log",dst=/var/log/access.log  \
      --mount type=bind,src="$(pwd)/state",dst=/var/lib/unit             \
      --mount type=bind,src="$(pwd)/nazo_api",dst=/www                   \
      -p 8900:8000 nazo_api                                           \
)

printf "unit started\n"
docker exec -ti $UNIT curl -X PUT --data-binary @/docker-entrypoint.d/config.json \
--unix-socket /var/run/control.unit.sock http://localhost/config