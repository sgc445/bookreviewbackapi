import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Home from "./components/Home";


function App() {
  return (
    <Router>
      <div>
        

        <Switch>
          <Route exact path="/">
            <h1>Book List!</h1>
            <Home />
          </Route>
          <Route path="/signup">
            <Signup />
          </Route>
          <Route path="/login">
            <Login />
          </Route>
        </Switch>

        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/signup">Signup</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </ul>
        </nav>

      </div>
    </Router>
  );
}

export default App;
