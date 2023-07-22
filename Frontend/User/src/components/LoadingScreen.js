import React from 'react';

const LoadingScreen = () => {
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75 z-50">
            <div className="flex items-center space-x-4 text-white">
                    <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-white rounded-full animate-bounce"></div>
                        <div className="w-3 h-3 bg-white rounded-full animate-bounce animation-delay-200ms"></div>
                        <div className="w-3 h-3 bg-white rounded-full animate-bounce animation-delay-400ms"></div>
                </div>
            </div>
        </div>
    );
};

export default LoadingScreen;
