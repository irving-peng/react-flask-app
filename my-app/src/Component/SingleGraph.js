import React from 'react';
import { useParams } from 'react-router-dom';
import {useState, useEffect} from 'react';
import './SingleGraph.css';

function SingleGraph() {
    // Get the label from the URL parameters
    const { label } = useParams();
    const [img, setImg] = useState('')
    let url = 'http://localhost:5000/' + label + '-plot'

    useEffect(() => {
        fetch(url)
        .then(response => response.blob())
        .then(blob =>{
            //create a logcal URL for the image
            const url = URL.createObjectURL(blob);
            setImg(url)
        })
        .catch(error => console.error('Error fetching the image:', error));
    }, [])
    //     useEffect(() => {
    //     fetch('http://localhost:5000/sale-plot')
    //     .then(response => response.blob())
    //     .then(blob =>{
    //         //create a logcal URL for the image
    //         const url = URL.createObjectURL(blob);
    //         setImg(url)
    //     })
    //     .catch(error => console.error('Error fetching the image:', error));
    // }, [])

    return (
    <div>
        <h1>Graph for: {label}</h1>
        <img src={img} alt="Loading ..."/> 
        {/* Additional logic and components to display the graph for the label */}
    </div>
    );
}

export default SingleGraph;