import { Schema, model, Document } from 'mongoose';

export interface ILoan extends Document {
  borrowerName: string;
  age: number;
  income: number;
  creditScore: number;
  loanAmount: number;
  loanTerm: number;
  hdiIndex: number;
  status: 'APPROVED' | 'REJECTED' | 'PENDING';
  probability: number;
  riskRating: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  createdAt: Date;
}

const LoanSchema = new Schema<ILoan>({
  borrowerName: { type: String, required: true, trim: true },
  age: { type: Number, required: true, min: 18 },
  income: { type: Number, required: true, min: 0 },
  creditScore: { type: Number, required: true, min: 300, max: 850 },
  loanAmount: { type: Number, required: true, min: 0 },
  loanTerm: { type: Number, required: true, min: 1 }, // in months
  hdiIndex: { type: Number, required: true, min: 0, max: 1 }, // Human Development Index (0.0 to 1.0)
  status: { 
    type: String, 
    enum: ['APPROVED', 'REJECTED', 'PENDING'], 
    default: 'PENDING' 
  },
  probability: { type: Number, default: 0.0 },
  riskRating: { 
    type: String, 
    enum: ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
    default: 'MEDIUM' 
  },
  createdAt: { type: Date, default: Date.now }
});

export const Loan = model<ILoan>('Loan', LoanSchema);
export default Loan;
