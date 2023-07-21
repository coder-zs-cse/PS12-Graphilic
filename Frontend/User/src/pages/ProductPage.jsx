import React from 'react';
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
  const recommendedProducts = [
    {
      id: '2',
      title: 'Recommended Product 1',
      category: 'Recommended Category 1',
    },
    {
      id: '3',
      title: 'Recommended Product 2',
      category: 'Recommended Category 2',
    },
    {
      id: '4',
      title: 'Recommended Product 3',
      category: 'Recommended Category 3',
    },
  ];

  return (
    <div>
      <ProductDetails product={selectedProduct} />
      <RecommendedProducts recommendedProducts={recommendedProducts} />
    </div>
  );
};

export default ProductPage;
