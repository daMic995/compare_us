"use client"
import Link from 'next/link'
import React, { useState, useEffect, useRef } from 'react';

import { ThreeDots } from 'react-loader-spinner';
import { BsChevronCompactLeft, BsChevronCompactRight, BsChevronUp, BsChevronDown } from 'react-icons/bs';
import { IoExtensionPuzzleOutline } from "react-icons/io5";
import { TbApi, TbBrandWalmart } from "react-icons/tb";
import { LiaCommentsSolid } from "react-icons/lia";
import { RxDotFilled } from 'react-icons/rx';
import StarRatings from 'react-star-ratings';
import { FaAmazon } from "react-icons/fa";

import { searchFeatures, scrollToFeature } from '../components/features';
import { prevSlide, nextSlide } from '../components/imageNav';
import StoreCheck from '../components/storeCheck';
import PopupCounter from '../components/popup';
import getUserId from '../components/getUserId';


function Loader({ isloading }: {readonly isloading: boolean }) {
  if (!isloading) {
    return null;
  }

  return (
    <ThreeDots
      height="60"
      width="60"
      radius="5"
      color="#000000"
      ariaLabel="three-dots-loading"
      wrapperStyle={{}}
      visible={true}
    />
  );
}

// Set up an empty comparison object
const COMP = { 
  title: '', 
  currency: '', 
  price: '', 
  description: '', 
  details: [''], 
  images: [''], 
  reviews: {count: '', rating: ''}, 
  url: '' 
}

export default function Home() {

  // Set up state variable for user ID
  const [user_id, setUser_id] = useState<string | null>(null);

  useEffect(() => {
    // Check if user ID is in local storage
    if (!('user_id' in localStorage)){
      getUserId().then(user_id => {
        if (user_id) {
          localStorage.setItem('user_id', user_id);
          setUser_id(user_id);
        }
      });
    }
    else {
      setUser_id(localStorage.getItem('user_id'));
    }
  }, []);



  // Set up state variable for loading
  const [loading, setLoading] = useState(false);

  // Set up state variables for product URLs and comparison results
  const [product_url1, setProduct_url1] = useState('');
  const [product_url2, setProduct_url2] = useState('');
  const [product1, setProduct1] = useState(COMP);
  const [product2, setProduct2] = useState(COMP);

  // Set up state variable for comparison status message
  const[statusMessage, setStatusMessage] = useState('');

  // Set up state variable for matched features
  const [matchedFeatures, setMatchedFeatures] = useState<{ [key: string]: [string, string] }>({});

  // Set up state variable for comparison status code
  const [status, setStatus] = useState<number | null>(null);
  
  // Set up state variable for scroll to section
  const [scrollToSection, setScrollToSection] = useState(false);

  // Set up state variables for product descriptions display
  const [showDescription1, setShowDescription1] = useState(false);
  const [showDescription2, setShowDescription2] = useState(false);

  // Set up state variables for image navigation
  const [currImg1Index, setCurrImg1Index] = useState(0);
  const [currImg2Index, setCurrImg2Index] = useState(0);

  // Set up state variable for search feature
  const [searchFeature, setSearchFeature] = useState('');

  // Set up state variable for search feature results
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [searchIndex, setSearchIndex] = useState(0);

  // Set up state variable for available comparisons
  const [available, setAvailable] = useState<number|null>(null);
  
  // Use useEffect to run only on client side
  useEffect(() => {
    // Retrieve variable from local storage else set to 5
    const storedAvailable = localStorage.getItem('available');
    setAvailable(storedAvailable ? parseInt(storedAvailable) : 5);
  }, []);

  // Update local storage when available changes
  useEffect(() => {
    if (available !== null) {
      console.log('Available: ' + available + ' ' + typeof available);
      localStorage.setItem('available', available.toString());
    }
  }, [available]);


  // Function to scroll with feature list
  const scrollWithFeatureList = (direction: number) => {
    const maxIndex = searchResults.length;

    // Scroll to the next or previous feature
    if (searchFeature !== '') {
      if (maxIndex > 0) {
        if (direction === 1 && searchIndex < maxIndex-1) {
          setSearchIndex(searchIndex + 1);
          scrollToFeature(searchResults[searchIndex + 1]);
        } else if (direction === -1 && searchIndex > 0) {
          setSearchIndex(searchIndex - 1);
          scrollToFeature(searchResults[searchIndex - 1]);
        }
      }
    } else if (direction === 1) {
      scrollToFeature('footer-section');
    } else if (direction === -1) {
      scrollToFeature('product-details-section');
    }
  };

  // Function to toggle product description display
  const showDescription = (index: number) => {
    if (index === 0) {
      setShowDescription1(!showDescription1);
    } else {
      setShowDescription2(!showDescription2);
    }
  };

  /**
   * Navigate to a specific slide by index.
   * Updates the current index to the specified slide index for the given product.
   * 
   * @param {number} index - The index of the slide to navigate to.
   * @param {number} proIndex - The index indicating which product's images are being navigated.
   */
  const goToSlide = (index: number, proIndex: number) => {
    // Check if we're navigating the first product's images
    if (proIndex === 0) {
      // Update the current index for the first product
      setCurrImg1Index(index);
    } else {
      // Update the current index for the second product
      setCurrImg2Index(index);
    }
  };

  /**
   * Handles form submission for product comparison.
   * Prevents default form submission behavior, sends a POST request to the comparison API,
   * and updates the state with the comparison results.
   * @param {React.FormEvent} e - The form submit event.
   */
  const compareSubmit = async (e: React.FormEvent) => {
    // Prevent default form submission behavior
    e.preventDefault();
    setLoading(true);

    try {
      // Set the API route for the comparison
      const apiRoute = '/api/python/compare';
      
      // Send a POST request to the comparison API with the product URLs as payload
      const response = await fetch(apiRoute, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          product1url: product_url1, 
          product2url: product_url2, 
          user_id: user_id 
        }),
      });

      // Parse the JSON response
      const data = await response.json();
      
      // Update the status state with the response status
      setStatus(data.status);
      
      // Check if the response status is 200
      if (data.status === 200){
        // Update the available state with the response available
        setAvailable(data.available_comparisons);
        // Update the status message state with the response message
        setStatusMessage(data.message)
        // Update the product states with the comparison results
        let comparedProducts = data.products;
        setProduct1(comparedProducts[0]);
        setProduct2(comparedProducts[1]);
        // Update the matched features state with the comparison results
        setMatchedFeatures(data.matched_features);
        // Set scrollToSection to true after successful response
        setScrollToSection(true);
      }

      else if (data.status === 403){
        // Update the available state with the response available
        setAvailable(data.available_comparisons);
        // Update the status message state with the response message
        setStatusMessage(data.message)
      }
      
      // Check if the response status is 400
      else {
        // Update the status message state with the response message
        setStatusMessage(data.message);
      }

    } catch (error) {
      // Update the status message state with the response message
      setStatusMessage('An error occurred. Please try again.');
      console.error('Error comparing products:', error);
      setStatus(404);
    }

    // Set loading state to false
    setLoading(false);
  };

  // Scroll Effect
  useEffect(() => {
    if (scrollToSection) {
      const navbarHeight = document.querySelector("nav")?.clientHeight || 0;
      
      // Scroll to the comparison section after the comparison is complete
      const comparisonSection = document.getElementById('results-section');
      if (comparisonSection) {
        window.scrollTo({ 
          behavior: 'smooth',
          top: comparisonSection.getBoundingClientRect().top + window.pageYOffset - navbarHeight + 4
         });
      }
    }
    setScrollToSection(false);
  }, [scrollToSection]);

  return (
    <div className="flex flex-col min-h-screen overflow-hidden">
      {/* Navbar */}
      <nav className="flex justify-between bg-white py-6 sm:px-2 sm:py-6 md:px-4 md:py-6 lg:px-6 lg:py-8 items-center shadow fixed top-0 left-0 right-0 z-10">
        {/* Logo */}
        <div className="flex flex-col ml-2 lg:md:flex-row items-center">
          <img className="block lg:md:sm:hidden" src="/compareprologo.png" alt="Logo" width={30} height={30}/>
          <h1 className="lg:text-xl md:text-lg sm:text-lg lg:md:sm:block hidden text-gray-800 font-bold">Compare Pro</h1>
          <img className='block lg:md:ml-2' src="/beta_icon.png" alt="Logo" width={35} height={25}/>
        </div>
        <div className="flex items-center">
          {/* Search feature */}
          <form id='search-form'
            className="flex items-center mr-8"
            onSubmit={(e) => {
              e.preventDefault();
              const newSearchResults = searchFeatures(searchFeature, matchedFeatures);
              setSearchResults(newSearchResults);
              setSearchIndex(0);
              if (newSearchResults.length > 0) {
                scrollToFeature(newSearchResults[0]);
              }
            }}>
            <button type='submit' aria-label="Search" className='focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 hover:bg-gray-300 p-2 rounded-lg'>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 pt-0.5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <input className="sm:ml-0 lg:ml-2 text-base sm:text-base md:text-base lg:text-base outline-none bg-transparent border-outline border border-outline rounded-lg px-2" 
            type="text" name="searchfeature" id="searchfeature" placeholder="Search Feature..." 
            value={searchFeature} onChange={(e) => setSearchFeature(e.target.value)}/>
          </form>

          <ul className="lg:px-4 md:sm:px-2 text-base flex items-center lg:space-x-6 md:sm:space-x-4 space-x-4 mr-2">
            <li className="font-semibold text-gray-700">
              <Link href="/feedback" title="Feedback Form">
                <LiaCommentsSolid className="h-6 w-6 text-gray-700" />
              </Link>
            </li>
            <li className="font-semibold text-gray-700">
              <Link href="#" title="API Documentation">
                <TbApi className="h-7 w-7 text-gray-700" />
              </Link>
            </li>
            <li>
              {/* Chrome Extension Link 
              https://github.com/daMic995/compare_us/tree/dev/extension*/}
              <a href="#" title="Chrome Extension">
                <IoExtensionPuzzleOutline className="h-6 w-6 text-gray-700"/>
              </a>
            </li>
          </ul>
        </div>
      </nav>
      
      {/* Main section */}
      <main className="flex flex-col items-center justify-between px-4 py-36 sm:py-36 md:sm:px-4 md:py-36 lg:p-48 h-auto w-screen bg-gradient-to-b from-white to-black via-gray-500 bg-radial">
        <div className='p-6'>
        <PopupCounter value={available}/>

          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-4xl text-white font-bold">Side-by-Side Comparison</h1>
        </div>
        {
        loading ? <Loader isloading={loading} /> :

        <form className="flex flex-col items-center justify-center lg:p-12 md:px-2 sm:p-4" onSubmit={compareSubmit}>
          <div className="lg:grid lg:grid-cols-2 lg:gap-6 py-6">
            <div className='flex items-center lg:mb-0 mb-4'>
              {StoreCheck(product_url1) /* Render the store icon*/}

              <input className={`${StoreCheck(product_url1) ? "ml-4" : "ml-0"} outline-none focus:outline-none focus:ring-2 focus:ring-gray-600 hover:ring-2 hover:ring-gray-600 border border-outline rounded-lg px-4 py-6 lg:w-96 w-72`}
              type="text" name="product1" id="product1" placeholder="Product 1" 
              required value={product_url1} onChange={(e) => setProduct_url1(e.target.value)}/>
            </div>
            <div className='flex items-center lg:mb-0 mb-2'>
              <input className={`${StoreCheck(product_url2) ? "mr-4" : "mr-0"} outline-none focus:outline-none focus:ring-2 focus:ring-gray-600 hover:ring-2 hover:ring-gray-600 border border-outline rounded-lg px-4 py-6 lg:w-96 w-72`}
              type="text" name="product2" id="product2" placeholder="Product 2" 
              required value={product_url2} onChange={(e) => setProduct_url2(e.target.value)}/>
              
              {StoreCheck(product_url2) /* Render the store icon*/}
            </div>
          </div>
          <div className='text-gray-400 text-sm mb-4'>You have {available} comparisons left</div>
          <button id="compare-button" type="submit" className={`${product_url1 && product_url2 ? 'bg-black hover:bg-blue-500' : 'bg-gray-300 disabled'} text-white font-bold py-5 px-8 rounded-lg focus:shadow-outline focus:outline-none transition duration-300 ease-in-out`}>
            Compare
          </button>
        </form>
        }

        <div className='text-xs mt-2 lg:md:sm:text-sm'>
        {!status && 
          <span className="text-gray-400">Only 
            <FaAmazon size={20} className='inline shadow m-2'/>and 
            <TbBrandWalmart size={22} className='inline shadow m-2'/>products are supported at this time. More coming soon!
          </span>}
        {status && status === 200 ? <p className="text-green-500">{statusMessage}</p> : <p className="text-red-500">{statusMessage}</p>}
        </div>

        <p className="mt-4 text-gray-400 text-sm">Powered by ComparePro</p>
      </main>

      {/* Comparison section */}
      {status === 200 ? 
      <section id="results-section" className='flex flex-col items-center justify-between px-0 lg:md:sm:px-6 lg:md:sm:py-6 w-screen bg-gradient-to-b from-black to-white via-gray-500 bg-radial'>
        <div className='flex flex-col items-center justify-between lg:md:sm:p-8'>
          <div id="product-cards" className="grid grid-cols-2 gap-6 lg:md:sm:py-4 px-2 lg:md:px-6">
            
            {/* Product cards */}
            {[product1, product2].map((product, productIndex) => (
            <div key={productIndex} id="product-card">
              <div className='flex flex-col bg-white rounded-lg'>
                <div id='product-image' className='flex flex-col rounded-lg justify-left px-0 lg:md:px-6 py-1'>
                  {/* Product image */}
                  <div className='flex flex-col py-12 max-w-[500px] h-[500px] w-full m-auto relative group'>
                    <div style={{backgroundImage: `url(${product.images[productIndex=== 0 ? currImg1Index : currImg2Index]})`, 
                    backgroundSize: 'contain', backgroundPosition: 'center', backgroundRepeat: 'no-repeat', width: '100%', height: '100%', position: 'relative'}}></div>
                    {/* Left arrow */}
                    <div className='hidden group-hover:block absolute top-[50%] -translate-x-0 -translate-y-[50%] left-0 text-2xl rounded-full bg-black/30 p-2 text-white cursor-pointer'>
                      <BsChevronCompactLeft onClick={() => {
                        const newIndex = prevSlide(product.images.length-1, productIndex, currImg1Index, currImg2Index);
                        goToSlide(newIndex, productIndex)}} size={30}/>
                    </div>
                    {/* Right arrow */}
                    <div className='hidden group-hover:block absolute top-[50%] -translate-x-0 -translate-y-[50%] right-0 text-2xl rounded-full bg-black/30 p-2 text-white cursor-pointer'>
                      <BsChevronCompactRight onClick={() => 
                        {const newIndex = nextSlide(product.images.length-1, productIndex, currImg1Index, currImg2Index);
                        goToSlide(newIndex, productIndex)}} size={30}/>
                    </div>
                    <div className='flex top-4 justify-center py-2 flex-wrap lg:md:px-0 px-4'>
                      {product.images.map((slide, slideIndex) => (
                        <div key={slideIndex} className='flex text-sm lg:md:sm:text-xl cursor-pointer' 
                        onClick={() => goToSlide(slideIndex, productIndex)}>
                            <RxDotFilled/>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div id='product-info' className='lg:md:sm:grid lg:md:sm:grid-cols-5 lg:md:sm:gap-6 lg:md:sm:px-6 px-4'>
                  {/* Product Title and Price */}
                  <div id='product-title' className='flex flex-col col-span-4'>
                    <p className='text-sm lg:text-lg md:text-base sm:text-sm font-bold text-black'>{product.title}</p>
                  </div>
                  <div id='product-price' className='flex flex-col lg:md:sm:text-right text-center mt-2 lg:md:sm:mt-0'>
                    <div id='price' className='bg-black rounded-md text-center py-2'>
                      <span className='text-white lg:sm:text-sm text-xs p-2'>{product.currency} {product.price}</span>
                    </div>
                    <a id='product-link' href={product.url} target="_blank" 
                    className='bg-blue-500 p-2 rounded-md text-white text-sm text-center font-semibold hover:underline lg:md:sm:mt-10 mt-2 py-2'>
                      Get It
                    </a>
                  </div>
                </div>

                <div id="product-rnd" className='flex flex-col rounded-lg justify-left lg:md:sm:px-6 p-4'>

                  <div id="product-rating" className='flex flex-col'>
                    {/* Product Rating */}
                    {product.reviews.rating === '' ? "No reviews" :
                      <div className='lg:md:grid lg:md:grid-cols-5'>
                        <div id='product-star-rating' className='flex flex-col lg:md:col-span-2'>
                        <StarRatings
                          rating={parseFloat(product.reviews.rating)}
                          starRatedColor="gold"
                          numberOfStars={5}
                          name='rating'
                          starDimension={window.innerWidth < 200 ? "5px" : "15px"}
                          starSpacing="2px"
                        />
                        </div>
                        <div id='product-number-rating' className='flex flex-col lg:md:col-span-1 lg:md:sm:py-0 py-4'>
                          <p className='text-sm text-gray-500'>{parseFloat(product.reviews.rating).toFixed(1)}</p>
                        </div>
                        <div id='product-description' className='flex flex-col lg:md:col-span-2 items-end lg:md:sm:py-0 py-2'>
                          <button type='button' onClick={() => showDescription(productIndex)} 
                          className='text-xs lg:md:sm:text-sm text-gray-500 hover:underline cursor-pointer'>
                            {productIndex === 0 ? showDescription1 ? 'Hide Description' : 'View Description' 
                                                : showDescription2 ? 'Hide Description' : 'View Description'}
                          </button>                      
                        </div>
                      </div>
                      }
                  </div>
                  
                  {
                  productIndex === 0 ? 
                    showDescription1 ? 
                      <div className='flex flex-col py-6 transition transform duration-700 ease-in-out'>
                      {/* Product Description */}
                      {product.description === "" ? 
                        <p className='text-xs lg:md:sm:text-base text-gray-500 p-2 border border-gray-200'>No description found</p> : 
                        <p className='text-xs lg:md:sm:text-base text-black p-2 border border-gray-200'>{product.description}</p>
                      }
                      </div> : null 
                  : showDescription2 ?                       
                      <div className='flex flex-col py-6 transition transform duration-700 ease-in-out'>
                      {/* Product Description */}
                      {product.description === "" ? 
                        <p className='text-xs lg:md:sm:text-base text-gray-500 p-2 border border-gray-200'>No description found</p> : 
                        <p className='text-xs lg:md:sm:text-base text-black p-2 border border-gray-200'>{product.description}</p>
                      }
                      </div> : null 
                  }

                </div>
              </div>
            </div>
            ))}
          </div>

          {/* Product Details Comparison */}
          <div id='product-details-section' className='flex flex-col px-2 lg:md:px-6 mt-12' style={{width: '100%'}}>
            <div className='mb-8'>
              <h2 className='text-2xl text-white text-center font-semibold mb-2'>All Specifications</h2>
              <p className='text-gray-400 text-sm md:text-base xl:lg:text-base text-center'>
                <span className='underline'>Disclaimer</span>: The specifications algorithm may innacurrately match features. 
                Make informed comparisons before purchasing items.
              </p>
            </div>
            {Object.entries(matchedFeatures).map(([key, value]) => (
              <div key={key} id={key.toLowerCase()} 
              className={`flex flex-col text-sm lg:md:sm:text-base text-center 
              ${key.toLowerCase() === searchResults[searchIndex] ? 'bg-blue-500 text-white' : 'bg-white text-black'}  
              px-6 py-4 mb-2 rounded-lg transition duration-300 ease-in-out`}>
                <strong>{key}</strong>
                <div className="grid grid-cols-2 gap-8 py-2">
                  <div className='flex flex-col border border-outline rounded-lg'>
                    <span>{value[0]}</span>
                  </div>
                  <div className='flex flex-col border border-outline rounded-lg'>
                    <span>{value[1]}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
        </div>
        <div className='fixed bottom-0 right-0 mb-6 mr-4 text-sm text-gray-500'>
          <div className='flex flex-col'>
            <button type='button' onClick={() => scrollWithFeatureList(-1) } className='focus:outline-none hover:text-indigo-700 hover:animate-bounce transition duration-300 ease-in-out mb-2'>
              <BsChevronUp size={30}/>
            </button>
          </div>
          <div className='flex flex-col'>
            {/* window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'}) */}
            <button type='button' onClick={() => scrollWithFeatureList(1) } className='focus:outline-none hover:text-indigo-500 hover:animate-bounce transition duration-300 ease-in-out'>
              <BsChevronDown size={30}/>
            </button>
          </div>
        </div>
      </section> : null}
      {/* Footer */}
      <footer id='footer-section' className='bg-white shadow flex flex-col items-center justify-center p-4 bottom-0 w-full'>
        <p className="mt-4 text-gray-400 text-sm mb-2">Powered by</p>
        <div className="flex flex-row items-center mb-2">
          <img className="block" src="/compareprologo.png" alt="Logo" width={30} height={30}/>
          <img className='block ml-2' src="/beta_icon.png" alt="Logo" width={35} height={25}/>
        </div>
      </footer>

    </div>
  )
}
