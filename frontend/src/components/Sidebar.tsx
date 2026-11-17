import React from 'react';
import { 
  LayoutDashboard, 
  MessageSquare, 
  GitFork, 
  Database, 
  FlaskConical, 
  BarChart3, 
  Compass, 
  FileText,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export type PageId = 
  | 'overview' 
  | 'playground' 
  | 'explorer' 
  | 'knowledge' 
  | 'benchmark' 
  | 'analytics' 
  | 'decision' 
  | 'documentation';

interface SidebarProps {
  activePage: PageId;
  onSelectPage: (page: PageId) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activePage, onSelectPage }) => {
  const navItems = [
    { id: 'overview' as PageId, label: 'Overview Dashboard', icon: LayoutDashboard, badge: 'Main' },
    { id: 'playground' as PageId, label: 'Chat Playground', icon: MessageSquare, badge: 'Interactive' },
    { id: 'explorer' as PageId, label: 'Architecture Explorer', icon: GitFork, badge: 'Visual' },
    { id: 'knowledge' as PageId, label: 'Knowledge Base', icon: Database, badge: '30+ FAQs' },
    { id: 'benchmark' as PageId, label: 'Benchmark Lab', icon: FlaskConical, badge: '50 Tests' },
    { id: 'analytics' as PageId, label: 'Analytics & Comparison', icon: BarChart3, badge: 'Metrics' },
    { id: 'decision' as PageId, label: 'Decision Guide', icon: Compass, badge: 'Advisor' },
    { id: 'documentation' as PageId, label: 'Project Documentation', icon: FileText, badge: 'Report' },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950 flex flex-col justify-between shrink-0 h-[calc(100vh-4rem)] sticky top-16 select-none">
      <div className="p-3 space-y-1">
        <div className="px-3 py-2 text-[11px] font-semibold tracking-wider uppercase text-slate-400">
          Navigation Modules
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectPage(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all group ${
                isActive
                  ? 'bg-gradient-to-r from-cyan-950/60 to-slate-900 text-cyan-300 border border-cyan-800/60 shadow-lg shadow-cyan-950/40'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 transition-transform group-hover:scale-110 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              <ChevronRight className={`w-3.5 h-3.5 transition-transform ${isActive ? 'text-cyan-400 translate-x-0.5' : 'text-slate-600 opacity-0 group-hover:opacity-100'}`} />
            </button>
          );
        })}
      </div>

      {/* Demonstration Banner */}
      <div className="p-4 m-3 rounded-xl bg-slate-900/70 border border-slate-800/80 text-[11px] text-slate-400 space-y-1.5">
        <div className="flex items-center gap-1.5 text-cyan-400 font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Demo University Data</span>
        </div>
        <p className="leading-relaxed">
          All university information is demonstration academic research data.
        </p>
      </div>
    </aside>
  );
};
