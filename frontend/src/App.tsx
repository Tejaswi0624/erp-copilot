import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from '@/components/layout/Layout'
import { Login } from '@/pages/Login'
import { Dashboard } from '@/pages/Dashboard'
import { Finance } from '@/pages/Finance'
import { HR } from '@/pages/HR'
import { Inventory } from '@/pages/Inventory'
import { Sales } from '@/pages/Sales'
import { CRM } from '@/pages/CRM'
import { Manufacturing } from '@/pages/Manufacturing'
import { Copilot } from '@/pages/Copilot'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      {/* Protected layout */}
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/finance" element={<Finance />} />
        <Route path="/hr" element={<HR />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/sales" element={<Sales />} />
        <Route path="/crm" element={<CRM />} />
        <Route path="/manufacturing" element={<Manufacturing />} />
        <Route path="/copilot" element={<Copilot />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
