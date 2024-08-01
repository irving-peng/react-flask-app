import React from 'react';
import './Result.css';
import {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom';

function Result() {

    const [item, setItem] = useState('');
    const[power, setPower] = useState(0)
    const[adjust, setAdjust] = useState('')
    const[comPlot, setComPlot] = useState('');

    const[buttons, setButtons] = useState([])

    useEffect(() => {
      fetch('http://localhost:5000/get-item')
        .then(response => response.json())
        .then(jsonData => setItem(jsonData.item))
        .catch(error => console.error('Error fetching data:', error));
    }, []);

    useEffect(() => {
        fetch('http://localhost:5000/combined-plot')
        .then(response => response.blob())
        .then(blob =>{
            //create a logcal URL for the image
            const url = URL.createObjectURL(blob);
            setComPlot(url)
        })
        .catch(error => console.error('Error fetching the image:', error));
    }, [])


    useEffect(() => {
      fetch('http://localhost:5000/adjustment')
        .then(response => response.json())
        .then(jsonData => {

          console.log(jsonData.high_power, jsonData.adjust_graph)
          setPower(jsonData.high_power)
          setAdjust(jsonData.adjust_graph)
          if (jsonData.adjust_graph !== ""){
            setButtons(jsonData.adjust_graph.split(", "))
            console.log('buttons: ' + buttons)
          }
        })
        .catch(error => console.error('Error fetching data:', error))
    }, [])

    const navigate = useNavigate();
    const handleButtonClick = (label) => {
      navigate(`/graph/${label}`); // Navigate to SingleGraph component with the label
    };

    return (
        <div className="image-gallery">
            
            <h2> Showing result for: {item} </h2>
            {adjust !== '' ? (
            <div>
              <h2>Check Unadjusted graph: </h2>
              {/* Render buttons from array */}
              <div className="button-container">
                {buttons.map((label, index) => (
                  <button key={index} className="result-button" onClick={() => handleButtonClick(label)}>
                    {label}
                  </button>
              ))}
              </div>
              <img src={comPlot} alt="Loading ..."/>
              <p>*{adjust} graph is adjusted to {power + 1} digits to all fit in one graph</p>

            </div>
            ) :
            (
            <div>
              <img src={comPlot} alt="Loading ..."/>  
            </div>
            )}
        </div>
    );
}

export default Result;






