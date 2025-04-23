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

# 网络名称
NETWORK_NAME="api"
# 网段
SUBNET="10.100.100.0/24"

# 容器IP
CONTAINER_IP="10.100.100.10"

if podman network ls | grep -q "$NETWORK_NAME"; then
  echo "Network '$NETWORK_NAME' already exists."
else
  echo "Network '$NETWORK_NAME' does not exist. Creating..."
  podman network create --subnet "$SUBNET" "$NETWORK_NAME"
  echo "Network '$NETWORK_NAME' created with subnet $SUBNET."
fi

printf "start unit\n"
export UNIT=$(                                                         \
      podman run -d                                                      \
      --name nazo_api                                                 \
      --mount type=bind,src="$(pwd)/config/",dst=/docker-entrypoint.d/   \
      --mount type=bind,src="$(pwd)/log/unit.log",dst=/var/log/unit.log  \
      --mount type=bind,src="$(pwd)/log/access.log",dst=/var/log/access.log  \
      --mount type=bind,src="$(pwd)/state",dst=/var/lib/unit             \
      --mount type=bind,src="$(pwd)/nazo_api",dst=/www                   \
      --network $NETWORK_NAME                                            \
      --ip $CONTAINER_IP                                                  \
      --privileged -v /dev/rtc:/dev/rtc:ro                               \
      --userns=keep-id                                                   \
      nazo_api                                           \
)

printf "unit started\n"
podman exec -ti $UNIT curl -X PUT --data-binary @/docker-entrypoint.d/config.json \
--unix-socket /var/run/control.unit.sock http://localhost/config