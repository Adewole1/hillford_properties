import React, { Component } from "react";
import { Link } from "react-router-dom";

import { Box } from "@mui/material";
import TopNavBar from "../components/navbar/TopNav/Topnav";
import BackToTop from "../components/navbar/TopNav/ScrollToTop";


const Home = () => {
  return (
    <React.Fragment>
      <TopNavBar />
      <Box sx={{}}>

      </Box>
      <BackToTop />
    </React.Fragment>
  );
};


export default Home;
