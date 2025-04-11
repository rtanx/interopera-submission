"use client";

import { useState, useEffect } from 'react';
import SalesDataTable from '@components/SalesDataTable';
import AIChatRoom from '@components/AIChatRoom';

export default function Home() {
  const [salesData, setSalesData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRep, setSelectedRep] = useState(null);

  useEffect(() => {
    // Fetch sales data from API
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/sales-reps');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setSalesData(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching sales data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <h1 className="text-2xl font-bold">Sales Dashboard</h1>
      </header>

      <main className="container mx-auto p-4">
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4" role="alert">
            <p className="font-bold">Error</p>
            <p>{error}</p>
          </div>
        )}

        <div className="flex flex-col md:flex-row gap-4">
          {/* Left side: Sales Data Table */}
          <div className="w-full md:w-3/5 bg-white shadow-md rounded-lg">
            <SalesDataTable
              salesData={salesData}
              isLoading={isLoading}
              onSelectRep={setSelectedRep}
              selectedRep={selectedRep}
            />
          </div>

          {/* Right side: AI Chat Room */}
          <div className="w-full md:w-2/5 bg-white shadow-md rounded-lg">
            <AIChatRoom selectedRep={selectedRep} />
          </div>
        </div>
      </main>
    </div>
  );
}