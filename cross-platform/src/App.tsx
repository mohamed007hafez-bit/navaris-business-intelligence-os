import { useMemo, useState } from 'react';
import { calculateNetFee, type FeeInputs } from './core/cash';

export default function App() {
  const [grossFee, setGrossFee] = useState('1000');
  const [directCosts, setDirectCosts] = useState('0');
  const [taxes, setTaxes] = useState('0');
  const [fxFees, setFxFees] = useState('0');

  const inputs: FeeInputs = {
    grossFee: Number(grossFee),
    directCosts: Number(directCosts),
    taxes: Number(taxes),
    fxFees: Number(fxFees)
  };
  const result = useMemo(() => calculateNetFee(inputs), [grossFee, directCosts, taxes, fxFees]);

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="compass">N</span><div><strong>NAVARIS</strong><small>BUSINESS OPERATIONS & DEVELOPMENT</small></div></div>
        <span className="badge">Cross-platform scaffold · v0.1</span>
      </header>
      <section className="hero">
        <p className="eyebrow">CASH ENGINE FIRST</p>
        <h1>Evidence → Calculation → Decision</h1>
        <p className="muted">A shared application shell for web, Windows desktop, and mobile. This demo calculation runs locally; it does not send data or messages.</p>
      </section>
      <section className="grid">
        <article className="panel">
          <p className="eyebrow">SHARED CORE · NET FEE</p>
          <h2>Commission calculator</h2>
          <p className="muted">Enter verified contractual inputs. This is a calculation demo, not proof of a deal or payment.</p>
          <label>Gross contractual fee<input inputMode="decimal" value={grossFee} onChange={e => setGrossFee(e.target.value)} /></label>
          <label>Direct costs<input inputMode="decimal" value={directCosts} onChange={e => setDirectCosts(e.target.value)} /></label>
          <label>Taxes / withholding<input inputMode="decimal" value={taxes} onChange={e => setTaxes(e.target.value)} /></label>
          <label>FX / payment fees<input inputMode="decimal" value={fxFees} onChange={e => setFxFees(e.target.value)} /></label>
          <div className="result"><span>Calculated net fee</span><strong>{result.toLocaleString(undefined, { maximumFractionDigits: 2 })}</strong></div>
        </article>
        <article className="panel">
          <p className="eyebrow">CONTROL STATUS</p>
          <h2>Deal qualification gates</h2>
          {['Source verified', 'Authorized buyer demand verified', 'Supplier and carrier qualified', 'Zero-capital structure confirmed', 'Fee agreement signed', 'Compliance checks passed', 'Economics validated'].map((item, index) => (
            <div className="gate" key={item}><span className="number">{String(index + 1).padStart(2, '0')}</span><span>{item}</span><span className="pending">PENDING</span></div>
          ))}
          <p className="notice">No gate is marked passed automatically. Cash collected remains 0 until payment evidence is reviewed.</p>
        </article>
      </section>
      <footer>Prototype only · No external APIs · No automatic communications · NAVARIS</footer>
    </main>
  );
}