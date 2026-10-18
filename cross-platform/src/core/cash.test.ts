import { describe, expect, it } from 'vitest';
import { calculateNetFee } from './cash';

describe('calculateNetFee', () => {
  it('subtracts direct costs, taxes, and fees from gross fee', () => {
    expect(calculateNetFee({ grossFee: 1000, directCosts: 100, taxes: 50, fxFees: 10 })).toBe(840);
  });

  it('returns zero when deductions equal gross fee', () => {
    expect(calculateNetFee({ grossFee: 100, directCosts: 60, taxes: 30, fxFees: 10 })).toBe(0);
  });

  it('rejects negative inputs', () => {
    expect(() => calculateNetFee({ grossFee: 100, directCosts: -1, taxes: 0, fxFees: 0 })).toThrow();
  });

  it('rejects NaN and infinite values', () => {
    expect(() => calculateNetFee({ grossFee: Number.NaN, directCosts: 0, taxes: 0, fxFees: 0 })).toThrow();
  });
});