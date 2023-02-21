import React, { Component } from "react";
import { withRouter, Link } from "react-router-dom";
import { connect } from "react-redux";

import axios from "axios";
import { setAxiosAuthToken } from "../../utils/Utils";
import {
  Alert,
  Container,
  // Button,
  Row,
  Col,
  Form,
  // FormControl
} from "react-bootstrap";
import Button from '@mui/material/Button';
import {
  Box,
  FormControlLabel,
  FormGroup,
  FormHelperText,
  TextField,
  Typography,
} from '@mui/material';

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useEffect, useState } from 'react';
import { LoadingButton } from '@mui/lab';
import Checkbox from '@mui/material/Checkbox';
// import { useForm, SubmitHandler } from 'react-hook-form';
// import { literal, object, string, TypeOf } from 'zod';
// import { zodResolver } from '@hookform/resolvers/zod';

import { createTheme, ThemeProvider, styled } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      light: '#6e43a3',
      main: '#4a148c',
      dark: '#330e62',
      contrastText: '#fff',
    },
    secondary: {
      light: '#ffcd38',
      main: '#ffc107',
      dark: '#b28704',
      contrastText: '#000',
    },
  },
});

class Signup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      first_name: "",
      last_name: "",
      position: "",
      phone_number: "",
      email: "",
      username: "",
      password: "",
      re_password: "",
      
      first_nameError: "",
      last_nameError: "",
      positionError: "",
      phone_numberError: "",
      emailError: "",
      usernameError: "",
      passwordError: "",
      re_passwordError: "",

      status: "",

      loading: false
    };
  }

  onChange = e => {
    e.preventDefault()
    this.setState({ [e.target.name]: e.target.value });
    // this.setState({ [e.target.name]+: "" })
  };

  // [position, setPosition] = useState('');

  // handlePosition = (event) => {
  //     setPosition(event.target.value);
  // };

  // handleChange = e => {
  //   console.log(e.target.value);
  //   this.setState({ [e.target.name] : e.target.value});
  // };


  onSignupClick = (e) => {
    e.preventDefault();
    this.setState({
      first_nameError: "",
      last_nameError: "",
      positionError: "",
      phone_numberError: "",
      emailError: "",
      usernameError: "",
      passwordError: "",
      re_passwordError: "",
      status: "",
      loading: true
    });

    const staffData = {
      first_name: this.state.first_name,
      last_name: this.state.last_name,
      position: this.state.position,
      phone_number: this.state.phone_number,
      email: this.state.email,
      username: this.state.username,
      password: this.state.password,
      re_password: this.state.re_password
    };

    setAxiosAuthToken(""); // send request with empty token
    axios
      .post("/accounts/staff/new", staffData)
      .then(response => {
        this.setState({ status: "success", loading: false });
      })
      .catch(error => {
        if (error.response) {
          if (error.response.data.hasOwnProperty("first_name")) {
            this.setState({ first_nameError: error.response.data["first_name"] });
          }
          if (error.response.data.hasOwnProperty("last_name")) {
            this.setState({ last_nameError: error.response.data["username"] });
          }
          if (error.response.data.hasOwnProperty("position")) {
            this.setState({ positionError: error.response.data["position"] });
          }
          if (error.response.data.hasOwnProperty("phone_number")) {
            this.setState({ phone_numberError: error.response.data["phone_number"] });
          }
          if (error.response.data.hasOwnProperty("username")) {
            this.setState({ usernameError: error.response.data["username"] });
          }
          if (error.response.data.hasOwnProperty("email")) {
            this.setState({ emailError: error.response.data["email"] });
          }
          if (error.response.data.hasOwnProperty("password")) {
            this.setState({ passwordError: error.response.data["password"] });
          }
          if (error.response.data.hasOwnProperty("re_password")) {
            this.setState({ re_passwordError: error.response.data["re_password"] });
          }
          if (error.response.data.hasOwnProperty("detail")) {
            this.setState({ status: "error" });
          }
        } else {
          this.setState({ status: "error" });
        };
        this.setState({ loading: false})
      });
  };

  render() {
    let errorAlert = (
      <Alert variant="danger">
        <Alert.Heading>Problem during staff account creation</Alert.Heading>
        Please try again or contact service support for further help.
      </Alert>
    );

    let successAlert = (
      <Alert variant="success">
        <Alert.Heading>Account created</Alert.Heading>
        <p>
          We send you an email with activation link. Please check your email.
        </p>
      </Alert>
    );

    // const [position, setPosition] = React.useState('');
    

    const form = (
      <ThemeProvider theme={theme}>
        <Box sx={{ maxWidth: '30rem'}}>
          <Typography variant='h4' component='h1' sx={{ mb: '2rem' }}>
            Staff Registration
          </Typography>
          <Box
            component='form'
            // noValidate
            autoComplete='off'
            // onSubmit={this.onSignupClick}
          >
            <TextField
              sx={{ mb: 2 }}
              label='First name'
              fullWidth
              required
              onChange={this.onChange}
              name = "first_name"
              variant = "standard"
              value={this.first_name}
              error={!!this.state.first_nameError}
              helperText={this.state.first_nameError}
            />

            <TextField
              sx={{ mb: 2 }}
              label='Last name'
              fullWidth
              required
              onChange = {this.onChange}
              name = "last_name"
              variant = "standard"
              value = {this.last_name}
              error={!!this.state.last_nameError}
              helperText={this.state.last_nameError}
            />

            <TextField
              sx={{ mb: 2 }}
              label='Email address'
              fullWidth
              required
              onChange = {this.onChange}
              variant = "standard"
              type = "email"
              name = "email"
              value = {this.email}
              error={!!this.state.emailError}
              helperText={this.state.emailError}
            />

            <TextField
              sx={{ mb: 2 }}
              label='Username'
              fullWidth
              // required
              onChange = {this.onChange}
              variant = "standard"
              type = "text"
              name="username"
              value = {this.username}
              error={!!this.state.usernameError}
              helperText={this.state.usernameError}
            />

            <TextField
              sx={{ mb: 2 }}
              label='Phone number'
              fullWidth
              required
              onChange = {this.onChange}
              variant = "standard"
              name = "phone_number"
              type = "text"
              value = {this.phone_number}
              error={this.state.phone_numberError}
              helperText={this.state.phone_numberError}
            />

            <FormControl fullWidth>
                <InputLabel>Position</InputLabel>
                <Select 
                  variant="standard" 
                  error={!!this.state.positionError}
                  helperText={this.state.positionError}
                  sx={{ mb: 2 }}
                  name = "position"
                  onChange = {this.onChange}
                  value = {this.state.position}
                >
                  <MenuItem value="">
                      <em>None</em>
                  </MenuItem>
                  <MenuItem value={"CEO"}>Chief Executive Officer</MenuItem>
                  <MenuItem value={"staff"}>Staff</MenuItem>
                  <MenuItem value={"realtor"}>Realtor</MenuItem>
                </Select>
            </FormControl>
  {/* 
            <Select
                // value={this.position}
                onChange={handleChange}
                label='Position'
                id="position-select"
                variant="standard"
                fullWidth
                name = "position"
                sx={{ mb: 2 }}
                error={!!this.state.positionError}
                helperText={this.state.positionError}
            >
                <MenuItem value="">
                    <em>None</em>
                </MenuItem>
                <MenuItem value={"CEO"}>Chief Executive Officer</MenuItem>
                <MenuItem value={"staff"}>Staff</MenuItem>
                <MenuItem value={"realtor"}>Realtor</MenuItem>
            </Select> */}

            <TextField
              sx={{ mb: 2 }}
              label='Password'
              fullWidth
              required
              onChange = {this.onChange}
              variant = "standard"
              name = "password"
              type = "password"
              error={!!this.state.passwordError}
              helperText={this.state.passwordError}
            />

            <TextField
              sx={{ mb: 2 }}
              label='Password confirmation'
              fullWidth
              required
              onChange = {this.onChange}
              variant = "standard"
              name = "re_password"
              type = "password"
              error={!!this.state.re_passwordError}
              helperText={this.state.re_passwordError}
            />

            <LoadingButton
              variant='contained'
              loading = {this.state.loading}
              loadingPosition="end"
              // loadingIndicator="Creating user"
              // color="primary"
              // fullWidth
              type='button'
              sx={{ py: '0.8rem', mt: '1rem', width: 0.4 }}
              onClick={this.onSignupClick}
            >
              Create user
            </LoadingButton>
          </Box>
        </Box>
      </ThemeProvider>
    );

    let alert = "";
    if (this.state.status === "error") {
      alert = errorAlert;
    } else if (this.state.status === "success") {
      alert = successAlert;
    }

    return (
      <Container>
        <Row>
          <Col md="6">
            {alert}
            {this.state.status !== "success" && form}
            <p className="mt-2">
              Already have account? <Link to="/login">Login</Link>
            </p>
          </Col>
        </Row>
      </Container>
    );
  }
}

Signup.propTypes = {};

const mapStateToProps = state => ({});

export default connect(mapStateToProps)(withRouter(Signup));