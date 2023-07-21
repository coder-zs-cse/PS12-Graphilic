import React from 'react';

const ProductsPage = ({ recommendation }) => {
    const asin_array = Object.keys(recommendation["res"])
  return (
    <div>
      <h2>Recommended Products</h2>
      <div className="recommended-products-container">
        {
       asin_array.map((id, index) => {
        //   const product = recommendation[title];
          return (
            <div key = {index} className="recommended-product">
              <h3>{id}</h3>
              {/* <p>Category: {product.category}</p> */}
            </div>
          );
        })
        }
      </div>
    </div>
  );
};

export default ProductsPage;
