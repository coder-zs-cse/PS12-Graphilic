import React, { useState } from 'react';
import './searchpage.css'; 
import SearchResults from '../components/SearchResults';
import Search from '../components/Search';

const SearchPage = () => {
  const [searchResults, setSearchResults] = useState([]);

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  return (
    <div className="app-container">
      <h1>Book Search App</h1>
      <Search onSearchResults={handleSearchResults} />
      {searchResults.length > 0 && <SearchResults searchResults={searchResults} />}
    </div>
  );
};

export default SearchPage;
