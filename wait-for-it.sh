# WAIT FOR REDIS - https://github.com/Hronom/wait-for-redis
echo "Start waiting for Redis fully start. Host '$REDIS_HOST', '$REDIS_PORT'..."
echo "Try ping Redis... "
PONG=`redis-cli -h $REDIS_HOST -p $REDIS_PORT ping | grep PONG`
while [ -z "$PONG" ]; do
    sleep 1
    echo "Retry Redis ping... "
    PONG=`redis-cli -h $REDIS_HOST -p $REDIS_PORT ping | grep PONG`
done
echo "Redis at host '$REDIS_HOST', port '$REDIS_PORT' fully started."

# WAIT FOR ELASTICSEARCH - https://gist.github.com/rochacbruno/bdcad83367593fd52005
echo "Start waiting for Elastic fully start. Host '$ELASTIC_HOST', '$ELASTIC_PORT'..."
echo "Try ping Elastic... "
is_ready() {
    eval "[ $(curl --write-out %{http_code} --silent --output /dev/null $ELASTIC_HOST:$ELASTIC_PORT/_cat/health?h=st) = 200 ]"
}
while ! is_ready; do
    sleep 1
    echo "Retry Elastic ping... "
done
echo "Elastic at host '$ELASTIC_HOST', port '$ELASTIC_PORT' fully started."
