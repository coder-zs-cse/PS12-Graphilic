import React from 'react';

const RecommendedProducts = ({ recommendedProducts }) => {
  return (
    <div>
      <h2>Recommended Products</h2>
      <div className="recommended-products-container">
        {recommendedProducts.map((product, index) => (
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
