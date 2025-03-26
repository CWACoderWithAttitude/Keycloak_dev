#!/bin/sh
#
# https://www.youtube.com/watch?v=fvxQ8bW0vO8
#
# https://www.keycloak.org/server/containers
#
# https://hub.docker.com/r/jboss/keycloak
#
#docker run --name keycloak \
# https://www.keycloak.org/observability/configuration-metrics
docker run  \
        -p 8080:8080 \
        -e KEYCLOAK_ADMIN=admin \
        -e KEYCLOAK_ADMIN_PASSWORD=admin \
        -e KC_HEALTH_ENABLED=true \
        -e KC_METRICS_ENABLED=true \
        quay.io/keycloak/keycloak \
        start-dev --metrics-enabled=true --health-enabled=true