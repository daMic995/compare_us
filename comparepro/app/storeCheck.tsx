"use client"
import { TbBrandWalmart } from "react-icons/tb";
import { FaAmazon } from "react-icons/fa";

function StoreCheck(url: string) {
    url = url.replace("https://", "");

    let store = null

    if (url.split("/")[0].split(".")[1] == "amazon"){
        store = <FaAmazon size={25} className='inline text-black'/>;
    }
    else if (url.split("/")[0].split(".")[1] == "walmart"){
        store = <TbBrandWalmart size={25} className='inline text-yellow-400'/>;
    }
    else if (url.split("/")[0].split(".")[1] == "bestbuy"){
        store = "bb";
    }
    return store;
};

export default StoreCheck