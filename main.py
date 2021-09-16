import requests

def main():
    start = ValidateProxy()
    start.check_proxy_list()

class ValidateProxy:
    
    __URL = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc&speed=medium&protocols=http%2Chttps"
    __IP_VALIDATOR = "https://icanhazip.com/"
    __ACTUAL_IP = requests.get(url=__IP_VALIDATOR).text
    
    def __init__(self):
        self.URL = ValidateProxy.__URL
        self.ip_validator = ValidateProxy.__IP_VALIDATOR
        self.actual_ip = ValidateProxy.__ACTUAL_IP
        self.proxy_list = self.get_proxys_list()

    def write_result(self, item:dict):
        with open("result.txt", "a") as f:
            f.write(f"{item['full']}\n")

    def get_proxys_list(self) -> list:
        try:
            self.response = requests.get(url=self.URL).json()
        except Exception:
            print("Somthing went wrong with proxylist.geonode.com")

        self.proxy_list = []

        for proxy in self.response["data"]:
            self.subresult = {"protocol": ["http", "https"], 
                            "ip": proxy['ip'],
                            "full": f"{proxy['ip']}:{proxy['port']}"}
            self.proxy_list.append(self.subresult)
        return self.proxy_list

    def check_proxy_list(self):
        for item in self.proxy_list:
            self.proxy = {item["protocol"][0]: f"{item['protocol'][0]}://{item['full']}",
                    item["protocol"][1]: f"{item['protocol'][1]}://{item['full']}"}
            
            try:
                print( "Trying: ", item["ip"])
                self.response = requests.get(url=self.ip_validator, proxies=self.proxy, timeout=10).text
                
                if self.response != self.actual_ip:
                    print(f"Valid proxy: {item['ip']}\n\n")
                    self.write_result(item)
                else:
                    print(f"Invalid proxy\n\n")
            
            except Exception:
                print(f"Connection Error!\n\n")



if __name__ == "__main__":
    main()