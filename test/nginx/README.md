
Files for testing Orchid connection through an NGINX reverse-proxy.

To run it:
* type `make`
* connect browser to `localhost:8080`

Configuration:
* `localhost:8080` listened by NGINX
* `localhost:4444` listened by Orchid
* Orchid configured to be accessed by address `localhost:8080/server`

Proxy is configured in NGINX with the configuration:

```
	location /server/ {
		proxy_pass http://127.0.0.1:4444;
	}

```
