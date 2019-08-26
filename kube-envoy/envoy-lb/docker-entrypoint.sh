#!/bin/sh
set -e

echo "Generating envoy.yaml config file..."
cat /tmp/envoy.yml.tmpl | envsubst \$ENVOY_LB_ALG,\$SERVICE_NAME > /etc/envoy.yaml

echo "Starting Envoy..."
/usr/local/bin/envoy -c /etc/envoy.yaml
