'use client'

import { useState } from 'react'
import { Menu } from 'lucide-react'
import { Sidebar } from './Sidebar'

export function AppLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex h-full min-h-screen bg-zinc-950 text-zinc-100">
      <Sidebar
        open={sidebarOpen}
        onToggle={() => setSidebarOpen(o => !o)}
      />

      <div
        className={`
          flex-1 flex flex-col
          transition-all duration-200 ease-in-out
          ${sidebarOpen ? 'md:ml-64' : 'ml-0'}
        `}
      >
        {/* Top bar */}
        <header className="flex items-center h-14 px-4 border-b border-zinc-800 shrink-0">
          {!sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(true)}
              className="text-zinc-500 hover:text-zinc-200 transition-colors"
              aria-label="Open sidebar"
            >
              <Menu size={20} />
            </button>
          )}
        </header>

        <main className="flex-1 flex flex-col">
          {children}
        </main>
      </div>
    </div>
  )
}
