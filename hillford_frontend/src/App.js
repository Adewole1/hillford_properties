import React, { Component } from "react";
import { Route, Routes, BrowserRouter as Router } from "react-router-dom";
import axios from "axios";
import { ToastContainer } from "react-toastify";
import { ThemeProvider, createTheme as MaterialTHeme } from "@mui/material/styles"
import { Container } from "@mui/material";

import Home from "./pages/home";
import "./App.css";


if (window.location.origin === "http://localhost:3000") {
  axios.defaults.baseURL = "http://127.0.0.1:8000";
} else {
  axios.defaults.baseURL = window.location.origin;
}


const customTheme = MaterialTHeme({
  palette: {
    primary: {
      main: "#460F56", 
      contrastText: '#fff',
    },
    secondary: {
      main: '#CEA032',
      contrastText: '#000',
    },
  },
  typography: {
    fontFamily: "'Outfit', sans-serif, 'Playfair Display', serif",
  },
})


class App extends Component {
  render() {
    return (
      <Router>
        <ThemeProvider theme={customTheme}>
        <ToastContainer hideProgressBar={true} newestOnTop={true} />
        <Container maxWidth="xl">
          <Routes>
            <Route exact path="/" element={<Home />} />
          </Routes>
        </Container>
        </ThemeProvider>
      </Router>
    );
  }
}

export default App;
