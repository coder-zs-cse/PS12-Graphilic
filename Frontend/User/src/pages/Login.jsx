import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Footer, Navbar } from "../components";

const Login = () => {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");

  const handleUsernameChange = (event) => {
    const inputUsername = event.target.value;
    setUsername(inputUsername);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
  
    // Check if the username is not empty before making the request
    if (!username) {
      return;
    }
  
    // Making the POST request to the backend
    fetch("http://localhost:5000/recommend_to_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: username }), // Sending the username as JSON data
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setMessage(data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
        setMessage("An error occurred. Please try again later.");
      });
  };
  

  return (
    <>
      <Navbar />
      <div className="container my-3 py-3">
        <h1 className="text-center">Login</h1>
        <hr />
        <div className="row my-4 h-100">
          <div className="col-md-4 col-lg-4 col-sm-8 mx-auto">
            <form onSubmit={handleSubmit}>
              <div className="my-3">
                <label htmlFor="display-4">Email address</label>
                <input
                  type="text"
                  className="form-control"
                  id="floatingInput"
                  placeholder="name@example.com"
                  value={username}
                  onChange={handleUsernameChange}
                />
              </div>
              <div className="my-3">
                <label htmlFor="floatingPassword display-4">Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="floatingPassword"
                  placeholder="Password"
                />
              </div>
              <div className="my-3">
                <p>
                  New Here?{" "}
                  <Link to="/register" className="text-decoration-underline text-info">
                    Register
                  </Link>{" "}
                </p>
              </div>
              <div className="text-center">
                <button className="my-2 mx-auto btn btn-dark" type="submit" disabled={!username}>
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
        {message && (
          <div className="row my-4 h-100">
            <div className="col-md-4 col-lg-4 col-sm-8 mx-auto">
              <p className="text-center">Message from Backend: {message}</p>
            </div>
          </div>
        )}
      </div>
      <Footer />
    </>
  );
};

export default Login;
