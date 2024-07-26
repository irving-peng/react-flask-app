// import React from 'react';
// import '../App.css';
// import {useState, useEffect} from 'react'

// function Result() {

//     // const [imageSrc, setImageSrc] = useState('');
//     const[salesPlot, setSalesPlot] = useState('');
//     const[marketPlot, setMarketPlot] = useState('');
//     const[pricePlot, setPricePlot] = useState('');
//     const[ratePlot, setRatePlot] = useState('');
//     const[comPlot, setComPlot] = useState('');

//     const [images, setImages] = useState([]);
        
//     useEffect(() => {
//         fetch('http://localhost:5000/sales-plot')
//         .then(response => response.blob())
//         .then(blob =>{
//             //create a logcal URL for the image
//             const url = URL.createObjectURL(blob);
//             setSalesPlot(url)
//         })
//         .catch(error => console.error('Error fetching the image:', error));
//     }, [])
//     useEffect(() => {
//         fetch('http://localhost:5000/market-plot')
//         .then(response => response.blob())
//         .then(blob =>{
//             //create a logcal URL for the image
//             const url = URL.createObjectURL(blob);
//             setMarketPlot(url)
//         })
//         .catch(error => console.error('Error fetching the image:', error));
//     }, [])
//     useEffect(() => {
//         fetch('http://localhost:5000/price-plot')
//         .then(response => response.blob())
//         .then(blob =>{
//             //create a logcal URL for the image
//             const url = URL.createObjectURL(blob);
//             setPricePlot(url)
//         })
//         .catch(error => console.error('Error fetching the image:', error));
//     }, [])
//     useEffect(() => {
//         fetch('http://localhost:5000/rate-plot')
//         .then(response => response.blob())
//         .then(blob =>{
//             //create a logcal URL for the image
//             const url = URL.createObjectURL(blob);
//             setRatePlot(url)
//         })
//         .catch(error => console.error('Error fetching the image:', error));
//     }, [])
//     useEffect(() => {
//         fetch('http://localhost:5000/combined-plot')
//         .then(response => response.blob())
//         .then(blob =>{
//             //create a logcal URL for the image
//             const url = URL.createObjectURL(blob);
//             setComPlot(url)
//         })
//         .catch(error => console.error('Error fetching the image:', error));
//     }, [])


//     return (
//         <div className="image-gallery">
//             <h1>Welcome to Result Page</h1>    
//             {/* {salesPlot && <img src={salesPlot} alt="Sales Plot"/>}
//             {marketPlot && <img src={marketPlot} alt="Market Plot"/>} */}
//             {/* {pricePlot && <img src={pricePlot} alt="Price Plot"/>} */}
//             {ratePlot && <img src={ratePlot} alt="Rate Plot"/>}
//             {/* {images.map((url, index) => (
//             <img key={index} src={url} alt={`Image ${index + 1}`} className="gallery-image" />
//         ))} */}
//         </div>
//     );
// }

// export default Result;


import React, { useState, useEffect } from 'react';
import ImageCarousel from './ImageCarousel';

function Result() {
  const [images, setImages] = useState([]);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const urls = [
          'http://localhost:5000/sales-plot',
          'http://localhost:5000/market-plot',
          'http://localhost:5000/price-plot',
          'http://localhost:5000/rate-plot',
          'http://localhost:5000/combined-plot',
        ];

        // Fetch images and handle blobs
        const imagePromises = urls.map(url => fetch(url).then(response => response.blob()));
        const blobs = await Promise.all(imagePromises);

        // Convert blobs to object URLs
        const imageUrls = blobs.map(blob => URL.createObjectURL(blob));
        console.log('Fetched image URLs:', imageUrls); // Log URLs for debugging
        setImages(imageUrls);
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    fetchImages();
  }, []); // Empty dependency array means this runs once on mount

  return (
    <div>
      <h1>Image Carousel</h1>
      <ImageCarousel images={images} />
    </div>
  );
}

export default Result;



