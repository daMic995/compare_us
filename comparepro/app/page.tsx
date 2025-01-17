"use client"
import { on } from 'events';
import Image from 'next/image'
import Link from 'next/link'
import React, { useState, useEffect, useRef } from 'react';
import { BsChevronCompactLeft, BsChevronCompactRight } from 'react-icons/bs';
import { RxDotFilled } from 'react-icons/rx';
import StarRatings from 'react-star-ratings';

export default function Home() {
  // Set up an empty comparison object
  const comp = {title: '', currency: '', price: '', description: '', details: [''], 
                images: [''], reviews: {count: '', rating: ''}, url: ''}

  // Set up state variables for product URLs and comparison results
  const [product_url1, setProduct_url1] = useState('');
  const [product_url2, setProduct_url2] = useState('');
  const [product1, setProduct1] = useState(comp);
  const [product2, setProduct2] = useState(comp);

  // Set up state variable for comparison status code
  const [status, setStatus] = useState<number | null>(null);
  
  // Set up state variable for scroll to section
  const [scrollToSection, setScrollToSection] = useState(false);
  const targetRef = useRef<HTMLDivElement>(null);

  // Set up state variables for product descriptions display
  const [showDescription1, setShowDescription1] = useState(false);
  const [showDescription2, setShowDescription2] = useState(false);

  // Set up state variables for image navigation
  const [currIndex1, setCurrIndex1] = useState(0);
  const [currIndex2, setCurrIndex2] = useState(0);

  const showDescription = (index: number) => {
    if (index === 0) {
      setShowDescription1(!showDescription1);
    } else {
      setShowDescription2(!showDescription2);
    }
  }
  /**
   * Navigate to the previous slide in the images list.
   * If the current index is the first one, wrap around to the last one.
   *
   * @param {string[]} imagesList - The list of images to navigate.
   * @param {number} proIndex - The index indicating which product's images are being navigated.
   */
  const prevSlide = (imagesList: string[], proIndex: number) => {
    // Determine if we're navigating the first product's images
    if (proIndex === 0) {
      // Check if the current index is the first slide
      const isFirstSlide = currIndex1 === 0;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isFirstSlide ? imagesList.length - 1 : currIndex1 - 1;
      // Update the current index for the first product
      setCurrIndex1(newIndex);
    } else {
      // Check if the current index is the first slide for the second product
      const isFirstSlide = currIndex2 === 0;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isFirstSlide ? imagesList.length - 1 : currIndex2 - 1;
      // Update the current index for the second product
      setCurrIndex2(newIndex);
    }
  }

  /**
   * Navigate to the next slide in the images list.
   * If the current index is the last one, wrap around to the first one.
   *
   * @param {string[]} imagesList - The list of images to navigate.
   * @param {number} proIndex - The index indicating which product's images are being navigated.
   */
  const nextSlide = (imagesList: string[], proIndex: number) => {
    // Determine if we're navigating the first product's images
    if (proIndex === 0) {
      // Check if the current index is the last slide
      const isLastSlide = currIndex1 === imagesList.length - 1;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isLastSlide ? 0 : currIndex1 + 1;
      // Update the current index for the first product
      setCurrIndex1(newIndex);
    } else {
      // Check if the current index is the last slide for the second product
      const isLastSlide = currIndex2 === imagesList.length - 1;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isLastSlide ? 0 : currIndex2 + 1;
      // Update the current index for the second product
      setCurrIndex2(newIndex);
    }
  }

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
      setCurrIndex1(index);
    } else {
      // Update the current index for the second product
      setCurrIndex2(index);
    }
  }

  /**
   * Handles form submission for product comparison.
   * Prevents default form submission behavior, sends a POST request to the comparison API,
   * and updates the state with the comparison results.
   * @param {React.FormEvent} e - The form submit event.
   */
  const compareSubmit = async (e: React.FormEvent) => {
    // Prevent default form submission behavior
    e.preventDefault();

    try {
      // Send a POST request to the comparison API with the product URLs as payload
      const response = await fetch('/api/python/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product1: product_url1, product2: product_url2 }),
      });

      // Parse the JSON response
      const data = await response.json();
      
      // Update the status state with the response status
      setStatus(data.status);

      // Update the product states with the comparison results
      setProduct1(data.product1);
      setProduct2(data.product2);

      // Set scrollToSection to true after successful response
      setScrollToSection(true);

    } catch (error) {
      console.error('Error comparing products:', error);
      setStatus(404);
    }
  };

  useEffect(() => {
    if (scrollToSection) {
      // Scroll to the comparison section after the comparison is complete
      const comparisonSection = document.getElementById('results-section');
      if (comparisonSection) {
        comparisonSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setScrollToSection(false);
  }, [scrollToSection]);

  return (
    <div className="flex flex-col min-h-screen overflow-hidden-x">
      {/* Navbar */}
      <nav className="flex justify-between bg-white px-20 py-8 items-center shadow fixed top-0 left-0 right-0 z-10">
        <h1 className="text-xl text-gray-800 font-bold">Compare Pro</h1>
        <div className="flex items-center">
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 pt-0.5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input className="ml-2 outline-none bg-transparent border-outline border border-outline rounded-lg px-2" type="text" name="search" id="search" placeholder="Filter Feature..." />
          </div>
          <ul className="px-4 flex items-center space-x-6">
            <Link href="/">
              <li className="font-semibold text-gray-700">Home</li>
            </Link>
            <li className="font-semibold text-gray-700">API</li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </li>
          </ul>
        </div>
      </nav>
      
      {/* Main section */}
      <main className="flex flex-col items-center justify-between p-48 h-screen w-screen bg-gradient-to-b from-white to-black via-gray-500 bg-radial">
        <div className='p-6'>
          <h1 className="text-4xl text-white font-bold">Side-by-Side Comparison Tool</h1>
        </div>
        <form className="flex flex-col items-center justify-between p-12" onSubmit={compareSubmit}>
          <div className="grid grid-cols-2 gap-6 py-6">
            <div className='flex flex-col'>
              <input className="outline-none focus:outline-none focus:ring-2 focus:ring-gray-600 hover:ring-2 hover:ring-gray-600 border border-outline rounded-lg px-4 py-6 w-96" 
              type="text" name="product1" id="product1" placeholder="Product 1" 
              required value={product_url1} onChange={(e) => setProduct_url1(e.target.value)}/>
            </div>
            <div className='flex flex-col'>
              <input className="outline-none focus:outline-none focus:ring-2 focus:ring-gray-600 hover:ring-2 hover:ring-gray-600 border border-outline rounded-lg px-4 py-6 w-96" 
              type="text" name="product2" id="product2" placeholder="Product 2" 
              required value={product_url2} onChange={(e) => setProduct_url2(e.target.value)}/>
            </div>
          </div>
          <button type="submit" className="bg-black hover:bg-black/80 text-white font-bold py-5 px-8 rounded-lg focus:shadow-outline focus:outline-none">Compare</button>
        </form>
      </main>

      {/* Comparison section */}
      {status === 200 ? 
      <div id="results-section" className='flex flex-col items-center justify-between px-6 py-8 w-screen bg-gradient-to-b from-black to-white via-gray-500 bg-radial'>
        <div className='flex flex-col items-center justify-between p-8'>
          <div className="grid grid-cols-2 gap-6 py-4 px-6">
            {/* Product cards */}
            {[product1, product2].map((product, productIndex) => (
            <div key={productIndex}>
              <div className='flex flex-col bg-white rounded-lg'>
                <div className='flex flex-col rounded-lg justify-left px-6 py-1'>
                  {/* Product image */}
                  <div className='flex flex-col py-12 max-w-[500px] h-[500px] w-full m-auto relative group'>
                    <div style={{backgroundImage: `url(${product.images[productIndex=== 0 ? currIndex1 : currIndex2]})`, 
                    backgroundSize: 'contain', backgroundPosition: 'center', backgroundRepeat: 'no-repeat', width: '100%', height: '100%', position: 'relative'}}></div>
                    {/* Left arrow */}
                    <div className='hidden group-hover:block absolute top-[50%] -translate-x-0 -translate-y-[50%] left-5 text-2xl rounded-full bg-black/30 p-2 text-white cursor-pointer'>
                      <BsChevronCompactLeft onClick={() => prevSlide(product.images, productIndex)} size={30}/>
                    </div>
                    {/* Right arrow */}
                    <div className='hidden group-hover:block absolute top-[50%] -translate-x-0 -translate-y-[50%] right-5 text-2xl rounded-full bg-black/30 p-2 text-white cursor-pointer'>
                      <BsChevronCompactRight onClick={() => nextSlide(product.images, productIndex)} size={30}/>
                    </div>
                    <div className='flex top-4 justify-center py-2'>
                      {product.images.map((slide, slideIndex) => (
                        <div key={slideIndex} onClick={() => goToSlide(slideIndex, productIndex)}>
                          <a className='text-xl cursor-pointer'>
                            <RxDotFilled/>
                          </a>
                        </div>
                    ))}
                    </div>
                  </div>
                </div>

                <div className='grid grid-cols-5 gap-6 px-6'>
                  {/* Product Title and Price */}
                  <div className='flex flex-col col-span-4'>
                    <p className='text-lg font-bold text-black'>{product.title}</p>
                  </div>
                  <div className='flex flex-col text-right'>
                    <div className='bg-black rounded-md text-center py-2'>
                      <span className='text-white text-sm p-2'>{product.currency} {product.price}</span>
                    </div>
                    <a href={product.url} className='text-white text-sm font-semibold hover:underline mt-10 py-2'>
                      <span className='bg-blue-500 p-2 rounded-md'>Get It</span>
                    </a>
                  </div>
                </div>

                <div className='flex flex-col rounded-lg justify-left p-6'>

                  <div className='flex flex-col'>
                    {/* Product Rating */}
                    {product.reviews.rating === '' ? "No reviews" :
                      <div className='grid grid-cols-5'>
                        <div className='flex flex-col col-span-2'>
                        <StarRatings
                          rating={parseFloat(product.reviews.rating)}
                          starRatedColor="gold"
                          numberOfStars={5}
                          name='rating'
                          starDimension="20px"
                          starSpacing="2px"
                        />
                        </div>
                        <div className='flex flex-col col-span-1'>
                          <p className='text-sm text-gray-500'>{product.reviews.rating}</p>
                        </div>
                        <div className='flex flex-col col-span-2 items-end'>
                          <button onClick={() => showDescription(productIndex)} 
                          className='text-sm text-gray-500 hover:underline cursor-pointer'>
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
                        <p className='text-md text-gray-500 p-2 border border-gray-200'>No description found</p> : 
                        <p className='text-md text-black p-2 border border-gray-200'>{product.description}</p>
                      }
                      </div> : null 
                  : showDescription2 ?                       
                      <div className='flex flex-col py-6 transition transform duration-700 ease-in-out'>
                      {/* Product Description */}
                      {product.description === "" ? 
                        <p className='text-md text-gray-500 p-2 border border-gray-200'>No description found</p> : 
                        <p className='text-md text-black p-2 border border-gray-200'>{product.description}</p>
                      }
                      </div> : null 
                  }

                </div>
              </div>
              <div className='flex flex-col bg-white rounded-lg mt-8 p-6'>
                <table className='p-2 '>

                {product.details.map((detail, index) => (
                  <tr key={index}>
                    {detail.split(':').map((part, partIndex) => (
                      <td>
                        {partIndex === 0 ? <b>{part}</b> : <span>{part}</span>}
                      </td>
                    ))}
                  </tr>
                ))}

              </table>
              </div>
            </div>
            ))}
          </div>
        </div>
        
      </div> : null}
    </div>
  )
}
