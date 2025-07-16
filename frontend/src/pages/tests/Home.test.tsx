import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../Home';

test('renders welcome message', () => {
  render(<Home />);
  const welcomeElement = screen.getByText(/Welcome to D'Agri Talk/i);
  expect(welcomeElement).toBeInTheDocument();
});

test('renders all feature cards', () => {
  render(<Home />);
  const traditionalKnowledge = screen.getByText(/Traditional Knowledge/i);
  const marketConnection = screen.getByText(/Market Connection/i);
  const communitySupport = screen.getByText(/Community Support/i);
  
  expect(traditionalKnowledge).toBeInTheDocument();
  expect(marketConnection).toBeInTheDocument();
  expect(communitySupport).toBeInTheDocument();
});

test('renders platform description', () => {
  render(<Home />);
  const description = screen.getByText(/Traditional Agricultural Knowledge Platform for Liberia/i);
  expect(description).toBeInTheDocument();
});
