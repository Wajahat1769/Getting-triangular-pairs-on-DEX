import requests
import json
import Arb
import time

#retrieving information from uniswap using graphql endpoint
def retrieving_uniswap_information():
    query="""
    {
   pools(orderBy:totalValueLockedETH,
   orderDirection: desc,
  first:500)
  {
    feeTier
    id
    totalValueLockedETH
    token0Price
    token1Price
    
    token0{ id symbol name decimals}
    token1{ id symbol name decimals}
  }
}
    """

    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    req = requests.post(url,json={'query':query})
    json_dict= json.loads(req.text)
    return json_dict

if __name__=="__main__":
    while 1:#C:\Users\Wajah\PycharmProjects\UniSwapV3\uniswap_surface_rates.json
        pairs = retrieving_uniswap_information()["data"]["pools"]
        triangular_pairs = Arb.structure_trading_pairs(pairs, limit=300)
        # get surface rates
        surface_rates_list = []
        for pairs in triangular_pairs:
            surface_rate = Arb.calc_triangular_arb_surface_rate(pairs, 10)
            if len(surface_rate) != 0:
                surface_rates_list.append(surface_rate)
                # print(surface_rate["pair1"], surface_rate["pair2"], surface_rate["pair3"], surface_rate["acquiredCoinT1"],
                #       surface_rate["acquiredCoinT2"], surface_rate["acquiredCoinT3"])

                # SAVE to JSON File
        if len(surface_rates_list) > 0:
            with open("uniswap_surface_rates.json", "w") as file:
                json.dump(surface_rates_list, file)
                print("file saved")
        time.sleep(120)


