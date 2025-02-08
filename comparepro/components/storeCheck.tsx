"use client"
import { TbBrandWalmart } from "react-icons/tb";
import { FaAmazon } from "react-icons/fa";

/**
 * A function that takes a URL and returns a JSX element representing the store where the item is from.
 * @param {string} url The URL of the item.
 * @returns {JSX.Element} A JSX element representing the store where the item is from.
 */
function StoreCheck(url: string) {
    url = url.replace("https://", "");

    // The store where the item is from
    let store: JSX.Element | null = null;

    // Check if the item is from Amazon
    if (url.split("/")[0].split(".")[1] === "amazon") {
        store = <FaAmazon size={25} className='inline text-black'/>;
    }
    // Check if the item is from Walmart
    else if (url.split("/")[0].split(".")[1] === "walmart") {
        store = <TbBrandWalmart size={25} className='inline text-yellow-400'/>;
    }
    // Check if the item is from Best Buy
    else if (url.split("/")[0].split(".")[1] === "bestbuy") {
        store = null;
    }

    return store;
};

export default StoreCheck