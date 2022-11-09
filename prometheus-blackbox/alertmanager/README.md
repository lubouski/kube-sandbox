## Alermanager prometheus rule
Alerting rules allow you to define alert conditions based on Prometheus expression language expressions and to send notifications about firing alerts to an external service.

### Configuration
To proper configure `kind: PrometheusRule`, we need to take an eye on: `metadata.labels: purpose: prometheus-prometheus` at our manifest. In order to get needed label we could check it at prometheus stack at `RuleSelector`.
```
# to search to RuleSelector
$ kubectl get prometheus prometheus -n monitoring -oyaml
# update if needed metadata.labels
``` 
Next we could configure proper `description and summary` using special variables as `$labels`.
```
# label available for particular expr could be found at Prometheus - Alertmanager UI.
$ kubectl -n monitoring  port-forward prometheus-prometheus-0 9090
# provide proper labels data which then will be substituted with proper data at alert destination teams or emails.
```
