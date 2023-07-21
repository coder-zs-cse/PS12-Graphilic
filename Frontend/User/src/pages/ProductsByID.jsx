import React from 'react';

const ProductsPage = ({ recommendation }) => {
  // Replace this with your actual product data or fetch the product details from the backend
  const productDetails = {
    "157794349X": {
      title: "Recommended Product 1",
      category: "Recommended Category 1",
    },
    "0892749504": {
      title: "Recommended Product 2",
      category: "Recommended Category 2",
    },
    "1577941829": {
      title: "Recommended Product 3",
      category: "Recommended Category 3",
    },
    // Add more product details as needed
  };

  return (
    <div>
      <h2>Recommended Products</h2>
      <div className="recommended-products-container">
        {recommendation.map((productId, index) => {
          const product = productDetails[productId];
          return (
            <div key={index} className="recommended-product">
              <h3>{recommendation}</h3>
              <p>Category: {product.category}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProductsPage;
