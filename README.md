## Usage (Dockerfile)
Clone the repo to local and cd into the folder
```
git clone https://github.com/Haoqing-Wu/VanitySearch.git
cd VanitySearch
```
Build dockerfile with the corresponding CCAP Version of your GPU(e.g. RTX40xx, CCAP=8.9; A100, CCAP=8.0), Compatibility table can be found on [Wikipedia](https://en.wikipedia.org/wiki/CUDA#GPUs_supported) or at the official NVIDIA web page of your product. 
```
docker build --build-arg CUDA=12.2.2 --build-arg CCAP=8.9 --tag 'vanity_search' .
```
Run the container
```
docker run -it --rm --gpus all -p 8090:8090 vanity_search
```
## Usage (Image)
```
sudo docker pull haoqingwu/vanity_search:40xx
sudo docker run -it --gpus all -p 8090:8090 haoqingwu/vanity_search:40xx 
```
## Test the response
Run request.py in the project folder locally
```
python request.py
```
Or send the address to 
Path: http://127.0.0.1/8090/aigic \
Method: POST \
input:
```
{
   "addr": "1YourTestAddress"
   }
```
output:
```
{
   "code": 200,
   "msg": "success"
   "content": "xxxx"
   }
```
