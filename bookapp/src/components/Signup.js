// Signup.js
import React from "react";
import axios from 'axios';

class Signup extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: "",
      password: "",
      email: "",
      successMessage:''
    };
  }

  handleUsernameChange = (event) => {
    this.setState({ username: event.target.value });
  };

  handlePasswordChange = (event) => {
    this.setState({ password: event.target.value });
  };

  handleEmailChange = (event) => {
    this.setState({ email: event.target.value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    // perform signup logic here

    const { username, password ,email} = this.state;

    axios.post('http://localhost:8000/create_user/', { username, password,email })
      .then(function (response) {
        console.log(":::::::::::::::",Object.keys(response.data).length);
        if (Object.keys(response.data).length=== 1) {
          // Request was successful, handle the data
          console.log(":::::::::::::::",response.data);

          this.setState({ successMessage: 'Sucessful in username creation' });



        } else {
          // Request failed, handle the error
          console.log('Request failed');
        }
      })
      .catch(error => {
        this.setState({ error: 'Username already exist' });
      });



  };

  render() {
    return (
      <div>
        <h2>Sign up</h2>
        <form onSubmit={this.handleSubmit}>
          <div>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" onChange={this.handleUsernameChange} />
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" onChange={this.handlePasswordChange} />
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" onChange={this.handleEmailChange} />
          </div>
          <button type="submit">Sign up</button>
        </form>
        {this.state.successMessage && <p>{this.state.successMessage}</p>}
      </div>
    );
  }
}

export default Signup;
