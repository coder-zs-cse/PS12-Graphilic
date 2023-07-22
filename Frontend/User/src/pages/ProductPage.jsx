import React, { useEffect, useState } from 'react';
import ProductDetails from '../components/ProductDetails';
import RecommendedProducts from '../components/RecommendedProducts';

const ProductPage = () => {
  // Replace this with actual data of the selected product
  

const selectedProduct = {
  id: '1',
  title: 'Selected Product Title',
  category: 'Selected Product Category',
  categories: ['Category 1', 'Category 2', 'Category 3'],
};

// Replace this with actual data of recommended products



return (
  <div>
    <ProductDetails product={selectedProduct} />
    <RecommendedProducts />
  </div>
);
};

export default ProductPage;
