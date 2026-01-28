import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { usePing } from './hooks/usePing'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const { status, error, data } = usePing()

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Cristales SaaS</h1>
      
      {/* Backend Ping Status */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <h2>Backend Connection</h2>
        {status === 'loading' && <p>🔄 Connecting...</p>}
        {status === 'success' && (
          <>
            <p>✅ Backend is <strong>ONLINE</strong></p>
            <pre style={{ backgroundColor: '#f0f0f0', padding: '10px', borderRadius: '4px' }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </>
        )}
        {status === 'error' && (
          <>
            <p>❌ Backend is <strong>OFFLINE</strong></p>
            <p style={{ color: 'red' }}>Error: {error}</p>
          </>
        )}
      </div>

      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
