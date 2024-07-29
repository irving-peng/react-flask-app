import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import ItemSelectionForm from './Component/ItemSelectionForm'
import Home from './Component/Home'
import Result from './Component/Result'
import SingleGraph from './Component/SingleGraph';


function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/form" element={<ItemSelectionForm />} />
      <Route path="/result" element={<Result />} />
      <Route path="/graph/:label" element={<SingleGraph/>} />
      </Routes>
    </Router>
  );
}

export default App;