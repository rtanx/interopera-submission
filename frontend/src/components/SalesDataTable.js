"use client"

import { useState } from 'react';
import { TabGroup, TabList, Tab, TabPanel, TabPanels } from '@headlessui/react';

function classNames(...classes) {
    return classes.filter(Boolean).join(' ');
}

export default function SalesDataTable({ salesData, isLoading, onSelectRep, selectedRep }) {
    const [activeTab, setActiveTab] = useState('overview');

    if (isLoading) {
        return (
            <div className="p-6 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading sales data...</p>
            </div>
        );
    }

    // Calculate total values for overview
    const totalWonDeals = salesData.reduce((total, rep) =>
        total + rep.deals.filter(deal => deal.status === "Closed Won").length, 0);

    const totalDealValue = salesData.reduce((total, rep) =>
        total + rep.deals.filter(deal => deal.status === "Closed Won")
            .reduce((sum, deal) => sum + deal.value, 0), 0);

    const handleSelectRep = (rep) => {
        if (rep.id === selectedRep?.id) {
            onSelectRep(null);
            setActiveTab('overview');
        } else {
            onSelectRep(rep);
            setActiveTab('details');
        }
    };

    return (
        <div className="p-4">
            <h2 className="text-xl font-semibold mb-4">Sales Representative Data</h2>

            <TabGroup selectedIndex={activeTab === 'overview' ? 0 : 1} onChange={(index) => setActiveTab(index === 0 ? 'overview' : 'details')}>
                <TabList className="flex rounded-lg bg-blue-100 p-1 mb-4">
                    <Tab className={({ selected }) =>
                        classNames(
                            'w-full rounded-lg py-2 text-sm font-medium leading-5',
                            'focus:outline-none focus:ring-2 ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            selected
                                ? 'bg-blue-600 text-white shadow'
                                : 'text-blue-700 hover:bg-white/[0.12] hover:text-blue-800'
                        )
                    }>
                        Overview
                    </Tab>
                    <Tab className={({ selected }) =>
                        classNames(
                            'w-full rounded-lg py-2 text-sm font-medium leading-5',
                            'focus:outline-none focus:ring-2 ring-offset-2 ring-offset-blue-400 ring-white ring-opacity-60',
                            selected
                                ? 'bg-blue-600 text-white shadow'
                                : 'text-blue-700 hover:bg-white/[0.12] hover:text-blue-800'
                        )
                    }>
                        Rep Details
                    </Tab>
                </TabList>

                <TabPanels>
                    {/* Overview Panel */}
                    <TabPanel>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                <h3 className="text-lg font-medium text-gray-700">Total Sales Reps</h3>
                                <p className="text-3xl font-bold text-blue-600">{salesData.length}</p>
                            </div>

                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                <h3 className="text-lg font-medium text-gray-700">Total Won Deals</h3>
                                <p className="text-3xl font-bold text-green-600">{totalWonDeals}</p>
                            </div>

                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                <h3 className="text-lg font-medium text-gray-700">Total Deal Value</h3>
                                <p className="text-3xl font-bold text-blue-600">${totalDealValue.toLocaleString()}</p>
                            </div>

                            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                <h3 className="text-lg font-medium text-gray-700">Regions</h3>
                                <p className="text-3xl font-bold text-purple-600">
                                    {new Set(salesData.map(rep => rep.region)).size}
                                </p>
                            </div>
                        </div>

                        <h3 className="font-medium text-gray-800 mb-2">Sales by Rep</h3>
                        <div className="overflow-x-auto overflow-y-auto max-h-70">
                            <table className="min-w-full min-h-1 bg-white">
                                <thead className="bg-gray-100">
                                    <tr>
                                        <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                        <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Region</th>
                                        <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Won</th>
                                        <th className="py-2 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Value</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {salesData.map((rep) => {
                                        const wonDeals = rep.deals.filter(d => d.status === "Closed Won");
                                        const totalValue = wonDeals.reduce((sum, deal) => sum + deal.value, 0);

                                        return (
                                            <tr
                                                key={rep.id}
                                                onClick={() => handleSelectRep(rep)}
                                                className={classNames(
                                                    "hover:bg-blue-50 cursor-pointer",
                                                    selectedRep?.id === rep.id ? "bg-blue-100" : ""
                                                )}
                                            >
                                                <td className="py-3 px-3">{rep.name}</td>
                                                <td className="py-3 px-3">{rep.region}</td>
                                                <td className="py-3 px-3">{wonDeals.length}</td>
                                                <td className="py-3 px-3">${totalValue.toLocaleString()}</td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </TabPanel>

                    {/* Rep Details Panel */}
                    <TabPanel>
                        {!selectedRep ? (
                            <div className="text-center py-10 text-gray-500">
                                Select a sales rep to view their details
                            </div>
                        ) : (
                            <div className="bg-white p-4 rounded-lg">
                                <div className="flex items-center mb-4">
                                    <div className="h-12 w-12 rounded-full bg-blue-500 flex items-center justify-center text-white text-xl font-semibold">
                                        {selectedRep.name.charAt(0)}
                                    </div>
                                    <div className="ml-4">
                                        <h3 className="text-lg font-medium">{selectedRep.name}</h3>
                                        <p className="text-sm text-gray-600">{selectedRep.role} - {selectedRep.region}</p>
                                    </div>
                                </div>

                                <div className="mb-6">
                                    <h4 className="text-sm font-medium text-gray-500 uppercase mb-2">Skills</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {selectedRep.skills.map((skill, index) => (
                                            <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div className="mb-6">
                                    <h4 className="text-sm font-medium text-gray-500 uppercase mb-2">Deals</h4>
                                    <div className="overflow-x-auto overflow-y-auto max-h-40">
                                        <table className="min-w-full">
                                            <thead className="bg-gray-50">
                                                <tr>
                                                    <th className="py-2 px-3 text-left text-xs font-medium text-gray-500">Client</th>
                                                    <th className="py-2 px-3 text-left text-xs font-medium text-gray-500">Value</th>
                                                    <th className="py-2 px-3 text-left text-xs font-medium text-gray-500">Status</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y divide-gray-200">
                                                {selectedRep.deals.map((deal, index) => (
                                                    <tr key={index}>
                                                        <td className="py-2 px-3">{deal.client}</td>
                                                        <td className="py-2 px-3">${deal.value.toLocaleString()}</td>
                                                        <td className="py-2 px-3">
                                                            <span className={classNames(
                                                                "px-2 py-1 rounded text-xs font-medium",
                                                                deal.status === "Closed Won" ? "bg-green-100 text-green-800" :
                                                                    deal.status === "Closed Lost" ? "bg-red-100 text-red-800" :
                                                                        "bg-yellow-100 text-yellow-800"
                                                            )}>
                                                                {deal.status}
                                                            </span>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-sm font-medium text-gray-500 uppercase mb-2">Clients</h4>
                                    <div className="space-y-2">
                                        {selectedRep.clients.map((client, index) => (
                                            <div key={index} className="p-3 border border-gray-200 rounded">
                                                <h5 className="font-medium">{client.name}</h5>
                                                <p className="text-sm text-gray-600">{client.industry}</p>
                                                <p className="text-sm text-blue-600">{client.contact}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}
                    </TabPanel>
                </TabPanels>
            </TabGroup>
        </div>
    );
}