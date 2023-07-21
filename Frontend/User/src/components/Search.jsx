import React, { useState } from 'react';
import axios from 'axios';

const Search = ({ onSearchResults }) => {
  const [queryTitle, setQueryTitle] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/search_query', {
        data: { query_title: queryTitle }
      });
      onSearchResults(response.data.similar_books);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={queryTitle}
        onChange={(e) => setQueryTitle(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default Search;
