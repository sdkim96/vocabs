import React from 'react';
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/home')({
  component: () => <div>Hello /home!</div>
})