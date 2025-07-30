"use client";

export function prevSlide (imagesListLength: number, proIndex: number, 
    currImg1Index: number, currImg2Index: number) : number {
    // Determine if we're navigating the first product's images
    if (proIndex === 0) {
      // Check if the current index is the first slide
      const isFirstSlide = currImg1Index === 0;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isFirstSlide ? imagesListLength : currImg1Index - 1;
      // Update the current index for the first product
      return newIndex;

    } else {
      // Check if the current index is the first slide for the second product
      const isFirstSlide = currImg2Index === 0;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isFirstSlide ? imagesListLength : currImg2Index - 1;
      // Update the current index for the second product
      return newIndex;
    }
};

export function nextSlide (imagesListLength: number, proIndex: number, 
    currImg1Index: number, currImg2Index: number) : number {
    // Determine if we're navigating the first product's images
    if (proIndex === 0) {
      // Check if the current index is the last slide
      const isLastSlide = currImg1Index === imagesListLength;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isLastSlide ? 0 : currImg1Index + 1;
      // Update the current index for the first product
      return newIndex;

    } else {
      // Check if the current index is the last slide for the second product
      const isLastSlide = currImg2Index === imagesListLength;
      // Calculate the new index, wrapping around if necessary
      const newIndex = isLastSlide ? 0 : currImg2Index + 1;
      // Update the current index for the second product
      return newIndex;
    }
};