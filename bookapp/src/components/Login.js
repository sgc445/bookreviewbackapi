// Login.js
import React from "react";
import axios from 'axios';


class Login extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      password: ""
    };
  }

  handleUsernameChange = (event) => {
    this.setState({ username: event.target.value });
  };

  handlePasswordChange = (event) => {
    this.setState({ password: event.target.value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    // perform login logic here
    const { username, password } = this.state;

    axios.post('http://localhost:8000/login/', { username, password })
      .then(function (response) {
        console.log(":::::::::::::::",Object.keys(response.data).length);
        if (Object.keys(response.data).length=== 2) {
          // Request was successful, handle the data
          console.log(":::::::::::::::",response.data);

        } else {
          // Request failed, handle the error
          console.log('Request failed');
        }
      })
      .catch(error => {
        this.setState({ error: 'Invalid email or password' });
      });
  };

  render() {
    return (
      <div>
        <h2>Login</h2>
        <form onSubmit={this.handleSubmit}>
          <div>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" onChange={this.handleUsernameChange} />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" onChange={this.handlePasswordChange} />
          </div>
          <button type="submit">Log in</button>
        </form>
      </div>
    );
  }
}

export default Login;
