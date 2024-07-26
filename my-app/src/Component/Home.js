import React from 'react';
import '../App.css';
import {useState, useEffect} from 'react'
//import { BrowserRouter as Router,  Route,Routes, Link } from 'react-router-dom';

import Deploy from'./Deploy/Deploy'
import ItemSelectionForm from './ItemSelectionForm';

function Home() {
  const [state, setState] = useState({})




  useEffect(() => {
    fetch("/api").then(response => {
      if(response.status ==200){
        return response.json()
      }
    }).then(data => {
      console.log("Fetched data:", data); // Log the data
      setState(data)
    })
    .catch(error => console.log(error))
  }, [])


  return (
    <div className="Home">
      <Deploy prop={state}/>
      
      {/* {salesPlot && <img src={salesPlot} alt="Sales Plot"/>} */}
      <h2>Select an Item</h2>
      <ItemSelectionForm />
    </div>
  );
}

export default Home;
