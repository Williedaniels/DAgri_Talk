import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Header from '../common/Header';

const HeaderWithRouter = () => (
  <BrowserRouter>
    <Header />
  </BrowserRouter>
);

test('renders D\'Agri Talk logo', () => {
  render(<HeaderWithRouter />);
  const logoElement = screen.getByText(/D'Agri Talk/i);
  expect(logoElement).toBeInTheDocument();
});

test('renders navigation links', () => {
  render(<HeaderWithRouter />);
  const knowledgeLink = screen.getByText(/Knowledge/i);
  const marketLink = screen.getByText(/Market/i);
  
  expect(knowledgeLink).toBeInTheDocument();
  expect(marketLink).toBeInTheDocument();
});