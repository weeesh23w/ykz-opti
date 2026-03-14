import urllib.request
url = "https://raw.githubusercontent.com/weeesh23w/ykz-opti/master/YKZ%20Optimizer.exe"
try:
    with urllib.request.urlopen(url) as response:
        print(f"Status: {response.status}")
        print(f"Content-Type: {response.getheader('Content-Type')}")
        print(f"Content-Length: {response.getheader('Content-Length')}")
        head = response.read(100)
        print(f"First 100 bytes: {head[:20]}")
except Exception as e:
    print(f"Error: {e}")
