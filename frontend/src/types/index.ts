export interface User {
    id: number;
    username: string;
    email: string;
    user_type: 'farmer' | 'elder' | 'buyer';
    location: string;
    created_at: string;
  }
  
  export interface KnowledgeEntry {
    id: number;
    title: string;
    content: string;
    language: string;
    crop_type: string;
    season: string;
    region: string;
    author: string;
    created_at: string;
    updated_at: string;
  }
  
  export interface MarketListing {
    id: number;
    crop_name: string;
    quantity: number;
    unit: string;
    price_per_unit: number;
    location: string;
    description: string;
    farmer: string;
    is_available: boolean;
    created_at: string;
  }