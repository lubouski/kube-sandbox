## Prometheus blackbox exporter
The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP, ICMP and gRPC. 

### Installation:
To install blackbox exporter we would use helm chart, additionally it's assumed that prometheus-operator is already installed in the cluster.
```
# Let's donwload and modify values.yaml from helm chart
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
$ helm show values  prometheus-community/prometheus-blackbox-exporter > values.yml
```
Then we could use `service monitor` configuration to educate `prometheus-oprator` which endpoint it needs to scrape.
```
$ vim values.yml
# For our example configuration, we adding tcp_check module to probe tcp endpoint
# Store the configuration as a `Secret` instead of a `ConfigMap`, useful in case it contains sensitive data
secretConfig: false
config:
  modules:
    http_2xx:
      prober: http
      timeout: 5s
      http:
        valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
        follow_redirects: true
        preferred_ip_protocol: "ip4"
    tcp_check:
      prober: tcp
      timeout: 5s
      tcp:
        preferred_ip_protocol: "ip4"

# Then we need to configure service monitor section
# selfMonitor.labels should be provided with appropriate promehteus-operator scraping labels
# additionally we need to add targets in our case it would be google for http probe and kafka for tcp on port 9093 
serviceMonitor:
  ## If true, a ServiceMonitor CRD is created for a prometheus operator
  ## https://github.com/coreos/prometheus-operator for blackbox-exporter itself
  ##
  selfMonitor:
    enabled: true
    additionalMetricsRelabels: {}
    additionalRelabeling: []
    labels:
      purpose: prometheus-prometheus
    interval: 30s
    scrapeTimeout: 30s

  ## If true, a ServiceMonitor CRD is created for a prometheus operator
  ## https://github.com/coreos/prometheus-operator for each target
  ##
  enabled: false

  # Default values that will be used for all ServiceMonitors created by `targets`
  defaults:
    additionalMetricsRelabels: {}
    additionalRelabeling: []
    labels: {}
    interval: 30s
    scrapeTimeout: 30s
    module: http_2xx
  ## scheme: HTTP scheme to use for scraping. Can be used with `tlsConfig` for example if using istio mTLS.
  scheme: http
  ## tlsConfig: TLS configuration to use when scraping the endpoint. For example if using istio mTLS.
  ## Of type: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#tlsconfig
  tlsConfig: {}
  bearerTokenFile:

  targets:
    - name: google
      url: https://www.google.com/
    - name: kafka
      url: strimzi-kafka-brokers.rtd.svc.cluster.local:9093
      module: tcp_check
```
### Grafana Dashboard:
Grafan has a nice feature of already build community dashboards, one of them could be used by us - [prometheus blackbox exporter](https://grafana.com/grafana/dashboards/14928-prometheus-blackbox-exporter)

### Documentation used:
[blackbox exporter configuration](https://github.com/prometheus/blackbox_exporter/blob/master/CONFIGURATION.md) 
[probe status](https://community.grafana.com/t/cant-get-prometheus-blackbox-exporter-tcp-to-show-probe-status/54235/2)
[example config](https://github.com/prometheus/blackbox_exporter/blob/master/example.yml)

