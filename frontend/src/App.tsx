import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>

        <div className="min-h-screen bg-[#0D0D0D] text-gray-100 flex">
          {/* Sidebar */}
          <aside className="w-64 bg-[#1A1A1A]/80 backdrop-blur-md p-4 space-y-3 rounded-r-2xl">
            <input
              placeholder="Search list..."
              className="w-full bg-[#0D0D0D] rounded-xl px-3 py-2 text-sm text-gray-300
              shadow-[inset_2px_2px_4px_rgba(0,0,0,0.6),inset_-2px_-2px_4px_rgba(255,255,255,0.05)] focus:outline-none"
            />
            <nav className="space-y-2">
              <button className="flex items-center gap-2 w-full px-3 py-2 rounded-xl bg-[#2A2A2A]">
                🌞 Today
              </button>
              <button className="flex items-center gap-2 w-full px-3 py-2 rounded-xl hover:bg-[#2A2A2A]">
                💼 Work
              </button>
              <button className="flex items-center gap-2 w-full px-3 py-2 rounded-xl hover:bg-[#2A2A2A]">
                📅 Upcoming <span className="ml-auto bg-orange-500 px-2 py-0.5 rounded-lg text-xs">Totoro</span>
              </button>
              <button className="flex items-center gap-2 w-full px-3 py-2 rounded-xl hover:bg-[#2A2A2A]">
                ✅ Completed
              </button>
            </nav>
          </aside>

          {/* Main content */}
          <main className="flex-1 flex justify-center items-center p-6">
            <div className="bg-[#1A1A1A]/80 backdrop-blur-md rounded-3xl p-6 w-full max-w-lg shadow-xl">
              <div className="flex justify-between items-center mb-4">
                <h1 className="text-xl font-bold">Upcoming</h1>
                <button className="bg-[#2A2A2A] rounded-full w-8 h-8 flex items-center justify-center hover:bg-[#3A3A3A]">
                  +
                </button>
              </div>

              <ul className="space-y-3">
                {["Promote Bento Cards v.2", "Bento Cards: UI Components", "Release Bento Cards", "Remove Illustrations"].map((task, i) => (
                  <li
                    key={i}
                    className="bg-[#0D0D0D] rounded-xl p-3 flex justify-between items-center shadow-[inset_2px_2px_4px_rgba(0,0,0,0.6),inset_-2px_-2px_4px_rgba(255,255,255,0.05)]"
                  >
                    <span>{task}</span>
                    <div className="flex gap-2">
                      <button className="hover:text-red-400">🗑️</button>
                      <button className="hover:text-blue-400">📋</button>
                      <button className="hover:text-gray-400">⋮</button>
                    </div>
                  </li>
                ))}
              </ul>

              <p className="text-gray-500 text-sm mt-4">Completed 1/5</p>
            </div>
          </main>
        </div>   
      </>
  )
}

export default App
