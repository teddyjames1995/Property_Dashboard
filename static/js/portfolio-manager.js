// Global Portfolio Manager - Shared across all dashboard pages
// Version: 2025-08-13

// Comprehensive portfolio data structure
window.PORTFOLIO_DATA = {
    'main': {
        name: 'Portfolio',
        type: 'commercial',
        value: 120000000, // £120M portfolio value
        data: {
            totalReturn: 15.2,
            capitalReturn: 8.5,
            incomeReturn: 6.7
        },
        properties: 5,
        tenants: 9
    },
    'sipp': {
        name: 'SIPP',
        type: 'pension',
        value: 45000000, // £45M portfolio value
        data: {
            totalReturn: 12.1,
            capitalReturn: 7.2,
            incomeReturn: 4.9
        },
        properties: 3,
        tenants: 4
    },
    'hands-on': {
        name: 'Hands On Mansfield',
        type: 'commercial',
        value: 85000000, // £85M portfolio value
        data: {
            totalReturn: 18.3,
            capitalReturn: 9.8,
            incomeReturn: 8.5
        },
        properties: 4,
        tenants: 6
    },
    'airbnbs': {
        name: 'AirBnBs',
        type: 'hospitality',
        value: 25000000, // £25M portfolio value
        data: {
            totalReturn: 22.4,
            capitalReturn: 12.2,
            incomeReturn: 10.2,
            // Hospitality-specific metrics
            revPAR: 145.30, // Revenue per Available Room
            adr: 185.50, // Average Daily Rate
            occupancyRate: 78.3, // Occupancy percentage
            bookingIncome: 2850000 // Annual booking income
        },
        properties: 8,
        guests: 1250 // Annual guests instead of tenants
    }
};

// Calculate aggregated "All" portfolio data
function calculateAggregatedData() {
    const individualPortfolios = ['main', 'sipp', 'hands-on', 'airbnbs'];
    let totalValue = 0;
    let weightedTotalReturn = 0;
    let weightedCapitalReturn = 0;
    let weightedIncomeReturn = 0;
    let totalProperties = 0;
    let totalTenants = 0;
    
    individualPortfolios.forEach(portfolioId => {
        const portfolio = window.PORTFOLIO_DATA[portfolioId];
        const weight = portfolio.value;
        totalValue += weight;
        
        weightedTotalReturn += (portfolio.data.totalReturn * weight);
        weightedCapitalReturn += (portfolio.data.capitalReturn * weight);
        weightedIncomeReturn += (portfolio.data.incomeReturn * weight);
        
        totalProperties += portfolio.properties;
        totalTenants += (portfolio.tenants || 0);
        if (portfolio.guests) totalTenants += portfolio.guests;
    });
    
    return {
        name: 'All Portfolios',
        type: 'aggregate',
        value: totalValue,
        data: {
            totalReturn: parseFloat((weightedTotalReturn / totalValue).toFixed(1)),
            capitalReturn: parseFloat((weightedCapitalReturn / totalValue).toFixed(1)),
            incomeReturn: parseFloat((weightedIncomeReturn / totalValue).toFixed(1))
        },
        properties: totalProperties,
        tenants: totalTenants
    };
}

// Add aggregated data to portfolios
window.PORTFOLIO_DATA['all'] = calculateAggregatedData();

// Global Portfolio Manager
window.PortfolioManager = {
    currentPortfolio: localStorage.getItem('selectedPortfolio') || 'all',
    
    // Get portfolio data
    getPortfolio: function(portfolioId) {
        return window.PORTFOLIO_DATA[portfolioId];
    },
    
    // Get current portfolio data
    getCurrentPortfolio: function() {
        return this.getPortfolio(this.currentPortfolio);
    },
    
    // Set current portfolio
    setCurrentPortfolio: function(portfolioId) {
        if (!window.PORTFOLIO_DATA[portfolioId]) {
            console.error('Portfolio not found:', portfolioId);
            return false;
        }
        
        this.currentPortfolio = portfolioId;
        localStorage.setItem('selectedPortfolio', portfolioId);
        
        // Trigger global portfolio change event
        this.triggerPortfolioChange(portfolioId);
        return true;
    },
    
    // Trigger portfolio change across all dashboard components
    triggerPortfolioChange: function(portfolioId) {
        console.log('🔄 Global portfolio change initiated:', portfolioId);
        
        // Update all portfolio dropdowns on the page
        document.querySelectorAll('select[id*="portfolio"]').forEach(select => {
            if (select.value !== portfolioId) {
                select.value = portfolioId;
                console.log('🔄 Updated dropdown:', select.id, 'to:', portfolioId);
            }
        });
        
        // Broadcast to registered update functions
        if (window.updateDashboardMetrics) {
            window.updateDashboardMetrics(portfolioId);
        }
        if (window.updateCharts) {
            window.updateCharts(portfolioId);
        }
        if (window.updateTopProperties) {
            window.updateTopProperties(portfolioId);
        }
        if (window.updateTopTenants) {
            window.updateTopTenants(portfolioId);
        }
        if (window.updatePerformanceMetrics) {
            window.updatePerformanceMetrics(portfolioId);
        }
        
        // Trigger custom event for other components to listen to
        window.dispatchEvent(new CustomEvent('portfolioChanged', {
            detail: { portfolioId: portfolioId, portfolioData: this.getPortfolio(portfolioId) }
        }));
        
        console.log('✅ Global portfolio change completed:', portfolioId);
    },
    
    // Initialize portfolio manager
    initialize: function() {
        console.log('🚀 Global Portfolio Manager initialized');
        console.log('Available portfolios:', Object.keys(window.PORTFOLIO_DATA));
        console.log('Current portfolio:', this.currentPortfolio);
        
        // Set up global event listeners for all portfolio dropdowns
        document.addEventListener('change', function(e) {
            if (e.target.matches('select[id*="portfolio"]')) {
                console.log('🎯 Portfolio dropdown changed:', e.target.id, 'to:', e.target.value);
                window.PortfolioManager.setCurrentPortfolio(e.target.value);
            }
        });
        
        // Also set up a mutation observer to detect dynamically added dropdowns
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        const portfolioSelects = node.querySelectorAll ? node.querySelectorAll('select[id*="portfolio"]') : [];
                        portfolioSelects.forEach(select => {
                            if (select.value !== window.PortfolioManager.currentPortfolio) {
                                select.value = window.PortfolioManager.currentPortfolio;
                                console.log('🔄 Initialized new dropdown:', select.id, 'with:', window.PortfolioManager.currentPortfolio);
                            }
                        });
                    }
                });
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
        
        return this;
    },
    
    // Utility functions
    formatCurrency: function(value) {
        if (value >= 1000000) {
            return `£${(value / 1000000).toFixed(0)}M`;
        } else if (value >= 1000) {
            return `£${(value / 1000).toFixed(0)}K`;
        } else {
            return `£${value.toLocaleString()}`;
        }
    },
    
    formatPercentage: function(value) {
        return `${value.toFixed(1)}%`;
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        window.PortfolioManager.initialize();
    });
} else {
    window.PortfolioManager.initialize();
}