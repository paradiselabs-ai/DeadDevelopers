import React, { useState } from 'react';
import { Inbox } from 'lucide-react';

const InboxButton = () => {
  const [unreadCount, setUnreadCount] = useState(5);
  const [isHovered, setIsHovered] = useState(false);
  
  const handleClick = () => {
    // Simulate opening the inbox
    alert(`Opening inbox with ${unreadCount} unread messages`);
  };
  
  const handleMarkAllRead = () => {
    setUnreadCount(0);
  };
  
  return (
    <div className="flex flex-col items-center justify-center space-y-6 p-8">
      <div className="text-2xl font-bold text-gray-800 mb-4">Notification Demo</div>
      
      <div 
        className={`relative inline-flex items-center justify-center p-3 rounded-full ${
          isHovered ? 'bg-blue-100' : 'bg-gray-100'
        } cursor-pointer transition-colors duration-200`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={handleClick}
      >
        <Inbox 
          size={28} 
          className={`${isHovered ? 'text-blue-600' : 'text-gray-600'} transition-colors duration-200`}
        />
        
        {unreadCount > 0 && (
          <div className="absolute -top-1 -right-1 flex items-center justify-center w-6 h-6 bg-red-500 text-white text-xs font-bold rounded-full animate-pulse">
            {unreadCount > 99 ? '99+' : unreadCount}
          </div>
        )}
      </div>
      
      <div className="flex space-x-4">
        <button 
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          onClick={() => setUnreadCount(prev => prev + 1)}
        >
          Add Message
        </button>
        
        <button 
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition-colors"
          onClick={handleMarkAllRead}
          disabled={unreadCount === 0}
        >
          Mark All Read
        </button>
      </div>
    </div>
  );
};

export default InboxButton;