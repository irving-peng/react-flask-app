import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { useNavigate } from 'react-router-dom';

function ItemSelectionForm() {
  // Use the useHistory hook to get access to the history instance
  const navigate = useNavigate();

  const [inputValue, setInputValue] = useState(''); // State for the input value
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch('/hub_item.csv'); // Path to CSV file in public folder
        const csvData = await response.text();
        //console.log('CSV Data:', csvData); // Log CSV data for debugging

        // Parse CSV data using PapaParse
        Papa.parse(csvData, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            //console.log('Parsed Data:', results.data); // Log parsed data for debugging
            const parsedItems = results.data.map((row) => row.itemName);
            setItems(parsedItems);
          },
        });
      } catch (error) {
        console.error('Error reading CSV file:', error);
      }
    };

    fetchItems();
  }, []);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Check if the input value exists in the parsed items
    if (items.includes(inputValue)) {
      // If the input value is found in the items, send it to the backend
      fetch('http://localhost:5000/submit-item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ item: inputValue }), // Send inputValue as item
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === 'success') {
            console.log('Item submitted successfully:', data.item);
            alert('Item selected successfully!');
            navigate('/result'); //navigate to result page
          } else {
            console.error('Submission error:', data.message);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    } else {
      // If the input value is not found in the items, show an alert
      alert('Input value not found in the CSV.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="item-input">Enter or search for an item:  </label>
        <input
          type="text"
          id="item-input"
          value={inputValue}
          onChange={handleInputChange}
          list="item-list" // Associate with datalist
          placeholder="Search or enter item..."
        />
        <datalist id="item-list">
          {items
            .filter((item) => item.toLowerCase().includes(inputValue.toLowerCase()))
            .map((item, index) => (
              <option key={index} value={item}>
                {item}
              </option>
            ))}
        </datalist>
      </div>
      <br/>
      <button type="submit">Submit</button>
    </form>
  );
}

export default ItemSelectionForm;
