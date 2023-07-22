import React, { useEffect,useState } from 'react';
import axios from 'axios';
import LoadingScreen from './LoadingScreen';
const getLastNumberFromURL = (url) => {
  // Split the URL by '/'
  const urlParts = url.split('/');

  // Get the last part of the URL, which is the number
  const lastPart = urlParts[urlParts.length - 1];

  // Ensure the last part is a number before returning it
  return /^\d+$/.test(lastPart) ? lastPart : '';
};
const RecommendedProducts = () => {
  const [ASIN, setASIN] = useState('');
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const currentURL = window.location.href;
  // console.log(typeof(getLastNumberFromURL(currentURL)));
  const fetchData = async () => {
    try{
      await fetch(`http://localhost:5000/recommend_item`,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"data": getLastNumberFromURL(currentURL)}),
      }).then((response) => response.json())
      .then((data) => {
        console.log(data);
        setRecommendedProducts(data);
      }
      );
      // console.log(response);

  }
  catch(error){
    console.log(error);
  }
  };
  useEffect(() => {
    console.log(currentURL);
    setASIN(getLastNumberFromURL(currentURL));
    setLoading(true);
    console.log("Loading")
    console.log("Done")
    setLoading(false);
  }, []);
  fetchData();
  return (
    
    <div>
      {loading && <LoadingScreen />}
      <h2>Recommended Products</h2>
      <div className="recommended-products-container">
        {recommendedProducts["ASINs"].map((product, index) => (
          <div key={index} className="recommended-product">
            <h3>{product.title}</h3>
            <p>Category: {product.category}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendedProducts;
