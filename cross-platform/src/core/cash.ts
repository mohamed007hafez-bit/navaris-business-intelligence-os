export interface FeeInputs {
  grossFee: number;
  directCosts: number;
  taxes: number;
  fxFees: number;
}

export function calculateNetFee(input: FeeInputs): number {
  const values = Object.values(input);
  if (!values.every(Number.isFinite)) {
    throw new Error('All fee inputs must be finite numbers.');
  }
  if (values.some(value => value < 0)) {
    throw new Error('Fee inputs cannot be negative.');
  }
  return input.grossFee - input.directCosts - input.taxes - input.fxFees;
}