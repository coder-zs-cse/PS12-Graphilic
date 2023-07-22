import React from 'react';
import { Link } from 'react-router-dom';

const SearchResults = ({ searchResults }) => {
  return (
    <div className="search-results-container">
      <h2>Search Results</h2>
      {searchResults.map((result, index) => (
        <Link to={`/ProductPage/${result.id}`} key={index} className="product-link" >
          <div className="search-result">
            <img
              src={`https://placeimg.com/200/300/book?${index}`}
              alt={`Book ${index + 1}`}
              className="book-image"
            />
            <h3>{result.title}</h3>
            <p>Category: {result.category}</p>
            <p>Categories: {result.categories.join(', ')}</p>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default SearchResults;
