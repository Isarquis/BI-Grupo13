import logo from './logo.svg';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from './Home';
import OtroEndpoint from './Otro';
import './App.css';
import NewsPredictor from './Predict';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/predict" element={<NewsPredictor />} />
        <Route path="/otro" element={<OtroEndpoint />} />
      </Routes>
    </Router>
  );
}
