# rzproxy

A local proxy help you chose the bset proxy from proxy pool


## Useage

Start rzproxy

	python run.py --host 127.0.0.1 --port 8399 --file-name proxy_pool.txt
	
Then use ("127.0.0.1:8399") as http proxy

	import requests
	requests.get(url, proixes={"http": "http://127.0.0.1:8399"})
	