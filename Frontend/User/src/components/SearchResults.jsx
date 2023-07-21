import React from 'react';

const SearchResults = ({ searchResults }) => {
  return (
    <div className="search-results-container">
      <h2>Search Results</h2>
      <br></br>
      {searchResults.map((result, index) => (
        <div key={index} className="search-result">
          <img
            src={`https://stacks-production-us-east-1-upload.imgix.net/38cd183a-3977-429c-971b-2d48285e992f.jpg?w=&h=280&dpr=3&auto=format&auto=compress&codec=mozjpeg&cs=strip`}
            alt={`Book ${index + 1}`}
            className="book-image"
          />
          <h3>{result.title}</h3>
          <p>Category: {result.category}</p>
          <p>Categories: {result.categories.join(', ')}</p>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;
