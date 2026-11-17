import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, PageId } from './components/Sidebar';
import { OverviewPage } from './pages/OverviewPage';
import { PlaygroundPage } from './pages/PlaygroundPage';
import { ExplorerPage } from './pages/ExplorerPage';
import { KnowledgeBasePage } from './pages/KnowledgeBasePage';
import { BenchmarkLabPage } from './pages/BenchmarkLabPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { DecisionGuidePage } from './pages/DecisionGuidePage';
import { DocumentationPage } from './pages/DocumentationPage';
import { api } from './services/api';

export const App: React.FC = () => {
  const [activePage, setActivePage] = useState<PageId>('overview');
  const [apiStatus, setApiStatus] = useState({
    configured: false,
    model: 'gemini-2.5-flash',
    faqsCount: 32
  });

  useEffect(() => {
    loadHealth();
  }, [activePage]);

  const loadHealth = async () => {
    try {
      const data = await api.fetchHealth();
      setApiStatus({
        configured: data.gemini_api_key_configured,
        model: data.gemini_model,
        faqsCount: data.faqs_count
      });
    } catch (e) {
      console.error("Health check error:", e);
    }
  };

  const getPageTitle = (id: PageId): string => {
    switch (id) {
      case 'overview': return 'Overview Dashboard';
      case 'playground': return 'Chat Playground';
      case 'explorer': return 'Architecture Explorer';
      case 'knowledge': return 'Knowledge Base';
      case 'benchmark': return 'Benchmark Lab';
      case 'analytics': return 'Analytics & Comparison';
      case 'decision': return 'Decision Guide';
      case 'documentation': return 'Project Documentation';
      default: return 'Architecture Lab';
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] flex flex-col font-sans">
      <Navbar apiStatus={apiStatus} activePageTitle={getPageTitle(activePage)} />

      <div className="flex flex-1">
        <Sidebar activePage={activePage} onSelectPage={setActivePage} />

        <main className="flex-1 p-6 lg:p-8 overflow-y-auto max-h-[calc(100vh-4rem)]">
          {activePage === 'overview' && (
            <OverviewPage
              onNavigateToBenchmark={() => setActivePage('benchmark')}
              onNavigateToPlayground={() => setActivePage('playground')}
            />
          )}
          {activePage === 'playground' && <PlaygroundPage />}
          {activePage === 'explorer' && <ExplorerPage />}
          {activePage === 'knowledge' && <KnowledgeBasePage />}
          {activePage === 'benchmark' && <BenchmarkLabPage />}
          {activePage === 'analytics' && <AnalyticsPage />}
          {activePage === 'decision' && <DecisionGuidePage />}
          {activePage === 'documentation' && <DocumentationPage />}
        </main>
      </div>
    </div>
  );
};
