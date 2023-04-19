import React from "react";
import axios from 'axios';


class Home extends React.Component {
    constructor(props) {
      super(props);
  
      this.state = {
        jsonData: "",
        error:"",
        isLoading: true,

      };
    }

    componentDidMount() {
          axios
          .get("http://192.168.0.18:8000/books/")
          .then((response) => {
            this.setState({ jsonData: response.data, isLoading: false });
          })
          .catch((error) => {
            this.setState({ error, isLoading: false });
          });
      }


      render() {
        const { jsonData, isLoading, error } = this.state;
    
        if (error) {
          return <p>{error.message}</p>;
        }
    
        if (isLoading) {
          return <p>Loading...</p>;
        }
    
        return (
          <div>
            <h1>Books</h1>
            <ul>
              {jsonData.map((book) => (
                <li key={book.title}>
                  {book.title} by {book.author}
                </li>
              ))}
            </ul>
          </div>
        );
      }


}

export default Home;
