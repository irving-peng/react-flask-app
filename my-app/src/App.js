import logo from './logo.svg';
import './App.css';
import {Deploy} from'./Component/Deploy/Deploy'
import {useState, useEffect} from 'react'
import ItemSelectionForm from './Component/ItemSelectionForm';

function App() {
  const [state, setState] = useState({})

  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    fetch("/api").then(response => {
      if(response.status ==200){
        return response.json()
      }
    }).then(data => setState(data))
    .then(error => console.log(error))
  }, {})

  useEffect(() => {
    // Fetch the plot image from the Python backend
    fetch('http://localhost:5000/plot')
      .then(response => response.blob())
      .then(blob => {
        // Create a local URL for the image
        const url = URL.createObjectURL(blob);
        setImageSrc(url);
      })
      .catch(error => console.error('Error fetching the image:', error));
  }, []);

  return (
    <div className="App">
      <Deploy prop={state}/>
      <h1>Sales Trend Visualization</h1>
      {imageSrc && <img src={imageSrc} alt="Data Visualization"/>}
      <h1>Select an Item</h1>
      <ItemSelectionForm />
    </div>
  );
}

export default App;
