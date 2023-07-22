import React from 'react';

const ProductsPage = ({ recommendation }) => {
  // Extract the ASINs and their corresponding values from the recommendation object
  const sortedASINs = Object.entries(recommendation["res"]).sort(([, valA], [, valB]) => valB - valA);
  const asin_array = sortedASINs.map(([asin]) => asin);

  return (
    <div>
      <h2>Recommended Products</h2>
      <div className="recommended-products-container">
        {
          asin_array.map((id, index) => {
            return (
              <div key={index} className="recommended-product">
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