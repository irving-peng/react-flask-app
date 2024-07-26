import React from 'react';
import ImageCarousel from './ImageCarousel';

function TestImageCarousel() {
  const testImages = [
    'https://via.placeholder.com/800x400?text=Image+1',
    'https://via.placeholder.com/800x400?text=Image+2',
    'https://via.placeholder.com/800x400?text=Image+3',
    'https://via.placeholder.com/800x400?text=Image+4',
    'https://via.placeholder.com/800x400?text=Image+5',
  ];

  return <ImageCarousel images={testImages} />;
}

export default TestImageCarousel;
